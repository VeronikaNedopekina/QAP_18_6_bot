import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Введены одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}. Помощь /help')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}. Помощь /help')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Помощь /help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base= json.loads(r.content)[keys[base]] * amount

        return total_base
