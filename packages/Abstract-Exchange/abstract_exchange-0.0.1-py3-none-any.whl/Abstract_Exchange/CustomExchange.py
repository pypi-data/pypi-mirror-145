from .functions import convert_baseAmount_to_quoteAmount
from ccxt.base.exchange import Exchange


class CustomExchange(Exchange):

    def __init__(self, config={}):
        super().__init__(config=config)
        self.tickers = dict()
        self.currencies = dict()
        self.apiName = None

    def init(self, apiName):
        self.apiName = apiName

    def load_tickers(self):
        self.tickers = super().fetch_tickers()
        return self.tickers

    def load_currencies(self):  # it is not needed for now
        self.currencies = super().fetch_currencies()
        return self.currencies

    def get_ask(self, symbol):
        try:
            return float(self.tickers[symbol]['ask'])
        except:
            return None

    def get_bid(self, symbol):
        try:
            return float(self.tickers[symbol]['bid'])
        except:
            return None

    def get_lastprice(self, symbol):
        try:
            return float(self.tickers[symbol]['last'])
        except:
            return None

    def get_fee(self, code):
        """ releated to child """
        try:
            return float(self.currencies[code]['fee'])
        except:
            return None

    def check_withdrawal(self, code):
        """ releated to child """
        return self.currencies[code]['payout']

    def check_deposit(self, code):
        """ releated to child """
        return self.currncies[code]['payin']

    def convert_currency(self, active, passive):
        quotes = {'DOGE', 'USDT', 'UST', 'USDC', 'TUSD',
                  'BTC', 'KCS', 'PAX', 'TRX', 'DAI', 'ETH'}
        active = active.split(' ')
        amount = float(active[0])
        active_code = active[1].upper()
        passive_code = passive.upper()
        
        if active_code in quotes:
            try:
                price = self.fetch_custom_price(f'{passive_code}/{active_code}')
                return float(amount / price)
            except:
                price = self.fetch_custom_price(f'{active_code}/{passive_code}')
                return float(amount * price)
        
        elif passive_code in quotes:
            price = self.fetch_custom_price(f'{active_code}/{passive_code}')
            return float(amount * price)


    def fetch_custom_total_balance(self, currency):
        return super().fetch_total_balance()[currency]

    def fetch_custom_free_balance(self, currency):
        return super().fetch_free_balance()[currency]

    def fetch_custom_price(self, symbol):
        return super().fetch_ticker(symbol)['last']
    
    def fetch_custom_ask(self, symbol):
        return super().fetch_ticker(symbol)['ask']
    
    def fetch_custom_bid(self, symbol):
        return super().fetch_ticker(symbol)['bid']

    def is_order_successfull(self, orderId):
        trades = super().fetch_my_trades()
        for trade in trades:
            if orderId == trade['info']['orderId']:
                return True
        return False

    def fetch_BaseMinSize(self, symbol):
        baseMinSize = self.fetch_market(symbol)['limits']['amount']['min']
        return baseMinSize

    def fetch_BaseMinSizeViaQuote(self, symbol):
        baseMinSize = self.fetch_BaseMinSize(symbol)
        quotePrice = self.fetch_custom_price(symbol)
        return convert_baseAmount_to_quoteAmount(baseMinSize, quotePrice)

    def fetch_market(self, symbol):
        for i in super().fetch_markets():
            if i['symbol'] == symbol:
                return i


# if __name__ == '__main__':
#     a = CustomExchange()
#     a.apiName = "baby"
#     print(a.__str__)
