from decimal import Decimal
import ccxt
import exchange_interface
import tools


class Bybit(exchange_interface.ExchangeInterface):

    def __init__(self, who):
        config = tools.fetch_dot_env()
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
