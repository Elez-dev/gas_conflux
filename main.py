from web3 import Web3
from requests.adapters import Retry
from threading import Thread
from merkly import Merkly
from tqdm import tqdm
from web3.middleware import geth_poa_middleware
import requests
import random
import time
import threading
import logging

# Settings ---------------------------------------------------------------

rpc_polygon = 'https://rpc.ankr.com/polygon'
rpc_celo    = 'https://rpc.ankr.com/celo'

CELO_CHAIN    = True
POLYGON_CHAIN = True

shuffle_wallets = True                 # мешать кошельки

number_of_transactions_min = 10         # Минимальное и
number_of_transactions_max = 20         # Максимальное количество транзакций

amount_from = 0.0000001                # Минимальная и
amount_to   = 0.00001                  # Максимальная сумма получения
amount_decimal = 9                     # округление

time_delay_min = 100                   # Максимальная и
time_delay_max = 150                   # Минимальная задержка между транзакциями

TIME_DELAY_MIN = 5                     # Минимальное и
TIME_DELAY_MAX = 10                    # Максимальное время задержки между потокам

TIME_DELAY_ACC_MIN = 500               # Минимальное и
TIME_DELAY_ACC_MAX = 1000              # Максимальное время задержки между АККАУНТАМИ

number_of_threads = 1                  # Количество потоков

# --------------------------------------------------------------------------------------------------


def shuffle(wallets_list):
    if shuffle_wallets is True:
        random.shuffle(wallets_list)
        numbered_wallets = list(enumerate(wallets_list, start=1))
    elif shuffle_wallets is False:
        numbered_wallets = list(enumerate(wallets_list, start=1))
    else:
        raise ValueError("\nНеверное значение переменной 'shuffle_wallets'. Ожидается 'True' or 'False'.")
    return numbered_wallets


def sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)
    with tqdm(
            total=delay,
            desc="💤 Sleep",
            bar_format="{desc}: |{bar:20}| {percentage:.0f}% | {n_fmt}/{total_fmt}",
            colour="green"
    ) as pbar:
        for _ in range(delay):
            time.sleep(1)
            pbar.update(1)


class Worker(Thread):
    def __init__(self):
        super().__init__()

    def run(self):

        log = logging.getLogger(threading.current_thread().name)
        console_out = logging.StreamHandler()
        basic_format1 = logging.Formatter('%(asctime)s : [%(name)s] : %(message)s')
        basic_format = logging.Formatter('%(asctime)s : %(message)s')
        console_out.setFormatter(basic_format1)
        file_handler = logging.FileHandler(f"{threading.current_thread().name}.txt", 'a', 'utf-8')
        file_handler.setFormatter(basic_format)
        log.setLevel(logging.DEBUG)
        log.addHandler(console_out)
        log.addHandler(file_handler)

        while keys_list:
            account = keys_list.pop(0)
            number = account[0]
            private_key = account[1]
            retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
            adapter = requests.adapters.HTTPAdapter(max_retries=retries)

            web3_arr = []

            session = requests.Session()
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            web3_polygon = Web3(Web3.HTTPProvider(rpc_polygon, request_kwargs={'timeout': 60}, session=session))
            web3_polygon.middleware_onion.inject(geth_poa_middleware, layer=0)

            if POLYGON_CHAIN is True:
                web3_arr.append(web3_polygon)

            session1 = requests.Session()
            session1.mount('http://', adapter)
            session1.mount('https://', adapter)
            web3_celo = Web3(Web3.HTTPProvider(rpc_celo, request_kwargs={'timeout': 60}, session=session1))
            web3_celo.middleware_onion.inject(geth_poa_middleware, layer=0)

            if CELO_CHAIN is True:
                web3_arr.append(web3_celo)

            address = web3_polygon.eth.account.from_key(private_key).address

            log.info('----------------------------------------------------------------------------')
            log.info(f'|   Сейчас работает аккаунт - {address}   |')
            log.info('----------------------------------------------------------------------------\n\n')

            str_number = f'{number} / {all_wallets}'

            number_of_transactions = random.randint(number_of_transactions_min, number_of_transactions_max)
            log.info(f'Количество транзакций - {number_of_transactions}\n')

            for i in range(number_of_transactions):
                web3 = random.choice(web3_arr)
                if web3 == web3_polygon:
                    name = 'Polygon'
                else:
                    name = 'Celo'

                merkl = Merkly(name, private_key, web3, str_number, log)
                log.info(f'Транзакция #{i+1}')
                amount = round(random.uniform(amount_from, amount_to), amount_decimal)
                merkl.get_gas(amount)
                sleep(time_delay_min, time_delay_max)
            session.close()
            delay = random.randint(TIME_DELAY_ACC_MIN, TIME_DELAY_ACC_MAX)
            log.info(f'Аккаунт завершен, сплю {delay} секунд и перехожу к следующему')
            time.sleep(delay)


if __name__ == '__main__':
    with open("private_keys.txt", "r") as f:
        list1 = [row.strip() for row in f if row.strip()]
    keys_list = shuffle(list1)
    all_wallets = len(keys_list)
    print(f'Number of wallets: {all_wallets}\n')
    for _ in range(number_of_threads):
        worker = Worker()
        worker.start()
        time.sleep(random.randint(TIME_DELAY_MIN, TIME_DELAY_MAX))
