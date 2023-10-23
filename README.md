[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&random=false&width=535&lines=%D0%9D%D0%B0%D0%B1%D0%B8%D0%B2%D0%B0%D0%B5%D0%BC+%D0%B4%D0%B5%D1%88%D1%91%D0%B2%D1%8B%D0%B5+%D1%82%D1%80%D0%B0%D0%BD%D0%B7%D1%8B+%D0%B2+L0+%D1%87%D0%B5%D1%80%D0%B5%D0%B7+Merkly)](https://git.io/typing-svg)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Софт отправляет выбранную сумму из POLYGON в CONFLUX

При минимальных значениях выходят затраты в 2 цента

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

НАСТРОЙКИ:

Приватные ключи в файл private_keys.txt

Всё настраиваем в файле main.py

shuffle_wallets — изменяет порядок кошельков

number_of_transactions_min - Минимальное количество транзакций

number_of_transactions_max - Максимальное количество транзакций

amount_from = 0.0000001 — минимальная сумма получения

amount_to   = 0.00001 — максимальная сумма получения

amount_decimal = 9  — округление отправляемых средств

time_delay_min = 50 — минимальная задержка между транзакциями

time_delay_max = 100 — максимальная задержка между транзакциями

TIME_DELAY_MIN = 5 — минимальное 

TIME_DELAY_MAX = 10 — максимальное время задержки между потокам

number_of_threads = 1 — количество одновременно запущенных кошельков(потоков)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

УСТАНОВКА:

git clone https://github.com/Elez-dev/gas_conflux.git

cd gas_conflux

pip install -r requirements.txt

python main.py