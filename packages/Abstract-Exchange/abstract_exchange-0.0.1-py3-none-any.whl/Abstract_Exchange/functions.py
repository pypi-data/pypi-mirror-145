from multiprocessing import Process


def filter_dict_keys(dict: dict, keys: list):
    i = 0
    dict_keys = list(dict.keys())
    while i < len(dict_keys):
        if dict_keys[i] not in keys:
            dict.pop(dict_keys[i])
        i += 1
    return dict


def dict_average(dict: dict):
    s = 0
    dict_values = dict.values()
    for i in dict_values:
        s += i
    ave = s / len(dict_values)
    return round(ave, 5)


def is_float(number):
    try:
        float(number)
        return True
    except:
        return False


def calculate_benefit_percentage(buyed_price=None, selled_price=None, percentage=None):
    if buyed_price and percentage:
        return buyed_price * ((100+percentage)/100)
    elif selled_price and percentage:
        return selled_price * ((100+percentage)/100)
    elif buyed_price and selled_price:
        return ((selled_price/buyed_price)*100)-100


def calculate_percentage(amount=None, totalAmount=None, percentage=None):
    if amount and percentage:
        return amount * (percentage/100)
    elif totalAmount and percentage:
        return totalAmount * (percentage/100)
    elif amount and totalAmount:
        return (amount / totalAmount) * 100


def convert_quoteAmount_to_baseAmount(quouteAmount, price):
    baseAmount = quouteAmount / price
    return baseAmount


def convert_baseAmount_to_quoteAmount(baseAmount, price):
    quoteAmount = baseAmount * price
    return quoteAmount


def convert_symbol(symbol: str, delemiter=""):
    quotes = {'DOGE', 'USDT', 'UST', 'USDC', 'TUSD',
              'BTC', 'KCS', 'PAX', 'TRX', 'DAI', 'ETH'}
    delemiters = {'-', ' ', '/'}
    symbol = symbol.strip()
    # delimeterd symbol
    for i in symbol:
        if i in delemiters:
            b = symbol.split(i)[0]
            q = symbol.split(i)[1]
            s = b + delemiter + q
            return s
    # undelimeterd symbol
    if symbol[-4:] in quotes:
        q = symbol[-4:]
        b = symbol[:-4]
        s = b + delemiter + q
        return s

    elif symbol[-3:] in quotes:
        q = symbol[-3:]
        b = symbol[:-3]
        s = b + delemiter + q
        return s


def reverse_side(side: str):
    side = side.capitalize()
    if side == "Buy":
        return "Sell"
    elif side == "Sell":
        return "Buy"
    return None


def precision_of_number(number):
    c = 0
    number = str(number)
    for i in range(len(number)-1, 0, -1):
        if number[i] == ".":
            return c
        c += 1


def run_in_parallel(fn, args):
    prcs = []
    for arg in args:
        p = Process(target=fn, args=arg)
        p.start()
        prcs.append(p)
    for p in prcs:
        p.join()
