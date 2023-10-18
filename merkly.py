from web3 import Web3
from wallet import Wallet
from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from eth_abi import encode
import time

abi = '''[
  {
    "inputs": [
      {
        "internalType": "uint16",
        "name": "_dstChainId",
        "type": "uint16"
      },
      {
        "internalType": "bytes",
        "name": "_toAddress",
        "type": "bytes"
      },
      {
        "internalType": "bytes",
        "name": "_adapterParams",
        "type": "bytes"
      }
    ],
    "name": "bridgeGas",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint16",
        "name": "_dstChainId",
        "type": "uint16"
      },
      {
        "internalType": "bytes",
        "name": "payload",
        "type": "bytes"
      },
      {
        "internalType": "bytes",
        "name": "_adapterParams",
        "type": "bytes"
      }
    ],
    "name": "estimateSendFee",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "nativeFee",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "zroFee",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]'''


class Merkly(Wallet):

    def get_gas(self, amount, retry=0):

        address = Web3.to_checksum_address('0x0e1f20075c90ab31fc2dd91e536e6990262cf76d')
        contract = self.web3.eth.contract(address=address, abi=abi)
        amount_wei = Web3.to_hex(encode(["uint"], [Web3.to_wei(amount, "ether")]))
        adapter_params = "0x0002000000000000000000000000000000000000000000000000000000000003d040" + amount_wei[2:] + self.address_wallet[2:]
        zro_payment_address = Web3.to_checksum_address('0x0000000000000000000000000000000000000000')

        try:
            fees = contract.functions.estimateSendFee(212, zro_payment_address, adapter_params).call()
            dick = {
                'from': self.address_wallet,
                'value': fees[0],
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            }
            contract_txn = contract.functions.bridgeGas(212, self.address_wallet, adapter_params).build_transaction(dick)
            self.sent_tx(contract_txn, 'Bridge from Polygon to Conflux')

        except TransactionNotFound:
            self.log.error('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.get_gas(amount, retry)

        except ConnectionError:
            self.log.error('Ошибка подключения к интернету или проблемы с РПЦ')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.get_gas(amount, retry)

        except Exception as error:
            if isinstance(error.args[0], dict):
                if 'insufficient funds' in error.args[0]['message']:
                    self.log.error('Ошибка, скорее всего нехватает комсы')
                    return 'balance'
                else:
                    self.log.error(error)
                    time.sleep(60)
                    retry += 1
                    if retry > 5:
                        return 0
                    self.get_gas(amount, retry)
            else:
                self.log.error(error)
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.get_gas(amount, retry)
