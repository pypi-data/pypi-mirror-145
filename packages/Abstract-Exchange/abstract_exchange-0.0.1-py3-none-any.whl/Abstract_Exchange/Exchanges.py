from time import mktime, sleep
from .CustomExchange import CustomExchange
from datetime import datetime
# from kucoin.client import
from ccxt.hitbtc import hitbtc as BaseHitbtc
from ccxt.kucoin import kucoin as BaseKucoin
from ccxt.bybit import bybit as BaseBybit
from pybit import usdt_perpetual
from concurrent.futures import ThreadPoolExecutor


class hitbtc(CustomExchange, BaseHitbtc):
    def __init__(self, config={}):
        super().__init__(config=config)

    def check_withdrawal(self, code):
        """ releated to child """
        return self.currencies[code]['payout']

    def check_deposit(self, code):
        """ releated to child """
        return self.currencies[code]['payin']


class kucoin(CustomExchange, BaseKucoin):
    def __init__(self, config={}):
        super().__init__(config=config)

        # self.trade = Trade(self.apiKey, self.secret, self.password)
        # self.user = User(self.apiKey, self.secret, self.password)

    def check_withdrawal(self, code):
        """ releated to child """
        return self.currencies[code]['info']['isWithdrawEnabled']

    def check_deposit(self, code):
        """ releated to child """
        return self.currencies[code]['info']['isDepositEnabled']


class bybit(CustomExchange, BaseBybit):
    def __init__(self, config={}):
        super().__init__(config=config)
        self.pybit = usdt_perpetual.HTTP(
            endpoint='https://api.bybit.com', api_key=self.apiKey, api_secret=self.secret)

    def is_in_position_size(self, symbol, side=None):  # check
        positions = self.pybit.my_position(symbol=symbol)['result']
        for pos in positions:
            if pos['size'] > 0 and (side == None or pos['side'] == side):
                return True
        return False

    def in_position_size(self, symbol):
        positions = self.pybit.my_position(symbol=symbol)['result']
        data = []
        for pos in positions:
            if pos['size'] > 0:
                data.append(pos)
        return data
    
    def in_position_size_orders(self, order_ids, symbols):
        orders = self.get_active_order_bulk(symbols, order_ids, order_status="Filled,PartiallyFilled")
        # sleep(.1)
        user_trade_records = self.user_trade_records_bulk(symbols=symbols, order_ids=order_ids)
        data = []
        for order in orders:
            in_position = 1
            for user_trade_record in user_trade_records:
                if order["order_id"] == user_trade_record["order_id"] and user_trade_record["closed_size"] == order["qty"]:
                    in_position = 0
                    break
            if in_position == 1:
                data.append(order)
        return data
                

    def in_position_size_bulk(self, symbols: list, max_in_parallel=40):  # chekc
        with ThreadPoolExecutor(max_workers=max_in_parallel) as executor:
            data = []
            executions = [
                executor.submit(
                    self.in_position_size,
                    **{"symbol": symbol}
                ) for symbol in symbols
            ]
        executor.shutdown()
        for execution in executions:
            data += execution.result()
        return data

    def is_in_active_order(self, symbol):
        active_orders = self.pybit.query_active_order(symbol=symbol)['result']
        if not(active_orders):
            return False
        return True

    def get_custom_leverage(self, symbol, side="Both"):
        data = self.pybit.my_position(symbol=symbol)['result']
        if side != "Both":
            for i in data:
                if i['side'] == side:
                    return i['leverage']
        else:
            return {"buy_leverage": data[0]["leverage"], "sell_leverage": data[1]["leverage"]}

    def set_custom_leverage(self, symbol, buy_leverage=None, sell_leverage=None):
        last_leverage = self.get_leverage(symbol=symbol, side="Both")
        buy_leverage = last_leverage["buy_leverage"] if buy_leverage == None else buy_leverage
        sell_leverage = last_leverage["sell_leverage"] if sell_leverage == None else sell_leverage
        self.pybit.set_leverage(
            symbol=symbol, buy_leverage=buy_leverage, sell_leverage=sell_leverage)

    def fetch_custom_free_balance(self, currency):
        return self.pybit.get_wallet_balance(coin=currency)['result'][currency]['available_balance']

    def get_active_order_bulk_one_page(self, symbols: list, page=1, limit=50, order_status="Created,Rejected,New,PartiallyFilled,Filled,Cancelled,PendingCancel", max_in_parallel=10):
        data = []
        with ThreadPoolExecutor(max_workers=max_in_parallel) as executor:
            executions = [
                executor.submit(
                    self.pybit.get_active_order,
                    **{"symbol": symbol, "order_status": order_status, "limit": limit, "page": page}
                ) for symbol in symbols
            ]
        executor.shutdown()
        for execution in executions:
            res = execution.result()["result"]["data"]
            if res != None:
                data += res
        return data

    def get_active_order_bulk(self, symbols: list, order_ids=[], order_status="Created,Rejected,New,PartiallyFilled,Filled,Cancelled,PendingCancel", max_in_parallel=10):
        data = []
        for page in range(1, 51):
            res = self.get_active_order_bulk_one_page(
                symbols=symbols, page=page, order_status=order_status, max_in_parallel=max_in_parallel)
            if not(res):
                break
            else:
                data += res
        if order_ids:
            data2 = []
            for order in data:
                if order["order_id"] in order_ids:
                    data2.append(order)
            return data2
        else:
            return data

    def closed_profit_and_loss_bulk_one_page(self, symbols: list, page=1, limit=50, start_time=0, end_time=mktime(datetime.timetuple(
            datetime.now())), max_in_parallel=40):
        data = []
        with ThreadPoolExecutor(max_workers=max_in_parallel) as executor:
            executions = [
                executor.submit(
                    self.pybit.closed_profit_and_loss,
                    **{"symbol": symbol, "start_time": start_time, "end_time": end_time, "limit": limit, "page": page}
                ) for symbol in symbols
            ]
        executor.shutdown()
        for execution in executions:
            res = execution.result()["result"]["data"]
            if res != None:
                data += res
        return data

    def closed_profit_and_loss_bulk(self, symbols: list, order_ids=[], start_time=0, end_time=mktime(datetime.timetuple(
            datetime.now())), max_in_parallel=40):
        data = []
        for page in range(1, 51):
            res = self.closed_profit_and_loss_bulk_one_page(
                symbols=symbols, page=page, start_time=start_time, end_time=end_time, max_in_parallel=max_in_parallel)
            if not(res):
                break
            else:
                data += res
        if order_ids:
            data2 = []
            for order in data:
                if order["order_id"] in order_ids:
                    data2.append(order)
            return data2
        else:
            return data

    def user_trade_records_bulk_one_page(self, symbols: list, page=1, limit=200, start_time=0, end_time=mktime(datetime.timetuple(
            datetime.now())), max_in_parallel=40):
        data = []
        with ThreadPoolExecutor(max_workers=max_in_parallel) as executor:
            executions = [
                executor.submit(
                    self.pybit.user_trade_records,
                    **{"symbol": symbol, "start_time": start_time, "end_time": end_time, "limit": limit, "page": page}
                ) for symbol in symbols
            ]
        executor.shutdown()
        for execution in executions:
            res = execution.result()["result"]["data"]
            if res != None:
                data += res
        return data

    def user_trade_records_bulk(self, symbols: list, order_ids=[], start_time=0, end_time=mktime(datetime.timetuple(
            datetime.now())), max_in_parallel=40):
        data = []
        for page in range(1, 51):
            res = self.user_trade_records_bulk_one_page(
                symbols=symbols, page=page, start_time=start_time, end_time=end_time, max_in_parallel=max_in_parallel)
            if not(res):
                break
            else:
                data += res
        if order_ids:
            data2 = []
            for order in data:
                if order["order_id"] in order_ids:
                    data2.append(order)
            return data2
        else:
            return data


if __name__ == '__main__':
    a = bybit({'apiKey': 'CSxcH3KzjGJqUrpwXe',
              'secret': 'iGLSmVrfhbDXMyICTc7TnVnfiYHqJpOKN2Mk'})
    print(a.pybit.my_position("DOGEUSDT"))
