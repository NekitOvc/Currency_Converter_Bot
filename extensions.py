import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base: # если 1-й параметр равен 2-му параметру
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.\
                \nВоспользуйтесь командой /values чтобы узнать список доступных валют.')

        try:
            quote_ticker = keys[quote]
        except KeyError: # обработка ошибки неверного ввода пользователем 1-го параметра
            raise ConvertionException(f'Не удалось обработать валюту {quote}.\
                \nВоспользуйтесь командой /values чтобы узнать список доступных валют.')
        
        try:
            base_ticker = keys[base]
        except KeyError: # обработка ошибки неверного ввода пользователем 2-го параметра
            raise ConvertionException(f'Не удалось обработать валюту {base}.\
                \nВоспользуйтесь командой /values чтобы узнать список доступных валют.')

        try:
            amount = float(amount)
        except ValueError: # обработка ошибки неверного ввода пользователем 3-го параметра
            raise ConvertionException(f'Не удалось обработать количество {amount}.\
                \nВ последнем параметре требуется ввести количество переводимой валюты')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base