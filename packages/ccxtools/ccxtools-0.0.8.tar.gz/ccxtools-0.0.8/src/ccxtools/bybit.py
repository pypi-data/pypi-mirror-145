from decimal import Decimal
import ccxt
from ccxtools import exchange


class Bybit(exchange.Exchange):

    def __init__(self, who, config):
        self.ccxt_inst = ccxt.bybit({
            'apiKey': config(f'BYBIT_API_KEY{who}'),
            'secret': config(f'BYBIT_SECRET_KEY{who}')
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
