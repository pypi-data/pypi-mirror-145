
class loader:

    def load_markets(exchanges=None, exchange=None):
        if exchange:
            exchange.load_markets()
            
        elif exchanges:
            for _ex in exchanges:
                _ex.load_markets()

    def load_tickers(exchanges=None, exchange=None):
        if exchange:
            exchange.load_tickers()
            
        elif exchanges:
            for _ex in exchanges:
                _ex.load_tickers()
    
    def load_markets_tickers(exchanges=None, exchange=None):
        if exchange:
            exchange.load_tickers()
            exchange.load_markets()
            
        elif exchanges:
            for _ex in exchanges:
                _ex.load_tickers()
                _ex.load_markets()