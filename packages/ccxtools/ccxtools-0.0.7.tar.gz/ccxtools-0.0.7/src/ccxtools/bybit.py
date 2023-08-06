from decimal import Decimal
import ccxt
from ccxtools import exchange


class Bybit(exchange.Exchange):

    def __init__(self, who, is_testing, config):
        config_word = 'BYBIT' if not is_testing else 'BYBIT_TESTNET'
        self.ccxt_inst = ccxt.bybit({
            'apiKey': config(f'{config_word}_API_KEY{who}'),
            'secret': config(f'{config_word}_SECRET_KEY{who}')
        })
        self.max_trading_qtys = self.get_max_trading_qtys()

    def get_max_trading_qtys(self):
        markets = self.ccxt_inst.fetch_markets()

        result = {}
        for market in markets:
            if not market['linear']:
                continue

            ticker = market['base']
            result[ticker] = Decimal(market['info']['lot_size_filter']['max_trading_qty'])

        return result
