import time


class Wallet:

    def __init__(self, private_key, web3, number, log):
        self.private_key = private_key
        self.web3 = web3
        self.number = number
        self.address_wallet = self.web3.eth.account.from_key(private_key).address
        self.log = log

    def sent_tx(self, contract, tx_lable):
        signed_txn = self.web3.eth.account.sign_transaction(contract, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.log.info('Отправил транзакцию')
        time.sleep(1)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300, poll_latency=2)
        if tx_receipt.status == 1:
            self.log.info(f'Транзакция смайнилась успешно')
        else:
            self.log.info('Транзакция сфейлилась, пытаюсь еще раз')
            time.sleep(60)
            raise ValueError('')

        self.log.info(f'[{self.number}] {tx_lable} || https://polygonscan.com/tx/{tx_hash.hex()}\n')
        return tx_hash.hex()
