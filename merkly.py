from web3 import Web3
from wallet import Wallet, exception_handler
from eth_abi import encode

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

    def __init__(self, chain_name, private_key, web3, number, log):
        super().__init__(private_key, web3, number, log)
        self.chain_name = chain_name

    @exception_handler()
    def get_gas(self, amount):

        if self.chain_name == 'Polygon':
            address = Web3.to_checksum_address('0x0e1f20075c90ab31fc2dd91e536e6990262cf76d')
            scan = 'https://polygonscan.com/tx/'
        else:
            address = Web3.to_checksum_address('0xc20a842e1fc2681920c1a190552a2f13c46e7fcf')
            scan = 'https://celoscan.io/tx/'

        contract = self.web3.eth.contract(address=address, abi=abi)
        amount_wei = Web3.to_hex(encode(["uint"], [Web3.to_wei(amount, "ether")]))
        adapter_params = "0x0002000000000000000000000000000000000000000000000000000000000003d040" + amount_wei[2:] + self.address_wallet[2:]
        zro_payment_address = Web3.to_checksum_address('0x0000000000000000000000000000000000000000')

        fees = contract.functions.estimateSendFee(212, zro_payment_address, adapter_params).call()
        dick = {
            'from': self.address_wallet,
            'value': fees[0],
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
        }
        contract_txn = contract.functions.bridgeGas(212, self.address_wallet, adapter_params).build_transaction(dick)
        self.sent_tx(contract_txn, f'Bridge from {self.chain_name} to Conflux', scan)
