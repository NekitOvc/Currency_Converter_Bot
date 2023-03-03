from config import AllConfiguration

import requests
import json
import logging

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # если 1-й параметр равен 2-му параметру
        if quote == base:
            logging.warning(f'Введены одинаковые параметры: {base}')
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.\
                \nВоспользуйтесь командой /currencies чтобы узнать список доступных валют.')

        # обработка ошибки неверного ввода пользователем 1-го параметра
        try:
            quote_ticker = AllConfiguration.keys[quote]
        except KeyError:
            logging.warning(f'Неверно введён 1-й параметр: {quote}')
            raise ConvertionException(f'Не удалось обработать валюту {quote}.\
                \nВоспользуйтесь командой /currencies чтобы узнать список доступных валют.')
        
        # обработка ошибки неверного ввода пользователем 2-го параметра
        try:
            base_ticker = AllConfiguration.keys[base]
        except KeyError:
            logging.warning(f'Неверно введён 2-й параметр: {base}')
            raise ConvertionException(f'Не удалось обработать валюту {base}.\
                \nВоспользуйтесь командой /currencies чтобы узнать список доступных валют.')

        # обработка ошибки неверного ввода пользователем 3-го параметра
        try:
            amount = float(amount)
        except ValueError:
            logging.warning(f'Неверно введён 3-й параметр: {amount}')
            raise ConvertionException(f'Не удалось обработать количество {amount}.\
                \nВ последнем параметре требуется ввести количество переводимой валюты')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[AllConfiguration.keys[base]]

        return total_base