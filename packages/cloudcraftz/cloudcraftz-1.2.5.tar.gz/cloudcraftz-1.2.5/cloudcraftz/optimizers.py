from .technical_indicators import *
from .plots import *
from .utils import *
import random

def sma_optimizer(price):
    """
    Pass a list of prices (or even an array)

    returns : a tuple of t1, t2 and the optimal signal (t1 and t2 are optimal time periods)
    """
    try:
        opt = -np.inf
        for i in range(1, 100):
            for j in range(1, 200):
                if i < j:
                    stock_short = simple_moving_average(price, {'periods': i})
                    stock_long = simple_moving_average(price, {'periods': j})

                    signal = get_signal_strategy(stock_short, stock_long)

                    pl, _, _ = agg_pl_max_dd(signal, price)

                    avg_pl = pl

                    if avg_pl > opt:
                        opt_signal = signal
                        opt = avg_pl
                        t1 = i
                        t2 = j

        return t1, t2, opt_signal
    except Exception as e:
        print(e)


def ema_optimizer(price):
    """
    Pass a list of prices (or even an array)

    returns : a tuple of t1, t2 and the optimal signal (t1 and t2 are optimal time periods)
    """
    try:
        opt = -np.inf
        for i in range(1, 100):
            for j in range(1, 200):
                if i < j:
                    stock_short = exponential_moving_average(price, {'periods': i})
                    stock_long = exponential_moving_average(price, {'periods': j})

                    signal = get_signal_strategy(stock_short, stock_long)

                    pl, _, _ = agg_pl_max_dd(signal, price)

                    avg_pl = pl

                    if avg_pl > opt:
                        opt_signal = signal
                        opt = avg_pl
                        t1 = i
                        t2 = j

        return t1, t2, opt_signal
    except Exception as e:
        print(e)


def rsi_optimizer(price):
    """
    Pass a list of prices (or even an array)

    returns : a tuple of t1, t2 and the optimal signal (t1 and t2 are optimal time periods)
    """
    try:
        opt = -np.inf
        for i in range(1, 100):
            for j in range(1, 200):
                if i < j:
                    stock_short = relative_strength_index(price, params={'periods': i, 'kind': simple_moving_average})
                    stock_long = relative_strength_index(price, params={'periods': j, 'kind': simple_moving_average})

                    signal = get_signal_strategy(stock_short, stock_long)

                    pl, _, _ = agg_pl_max_dd(signal, price)

                    avg_pl = pl

                    if avg_pl > opt:
                        opt_signal = signal
                        opt = avg_pl
                        t1 = i
                        t2 = j

        return t1, t2, opt_signal
    except Exception as e:
        print(e)


def roc_optimizer(price):
    """
    Pass a list of prices (or even an array)

    returns : a tuple of t1, t2 and the optimal signal (t1 and t2 are optimal time periods)
    """
    try:
        opt = -np.inf
        for i in range(1, 100):
            for j in range(1, 200):
                if i < j:
                    stock_short = ROC(price, {'periods': i})
                    stock_long = ROC(price, {'periods': j})

                    signal = get_signal_strategy(stock_short, stock_long)

                    pl, _, _ = agg_pl_max_dd(signal, price)

                    avg_pl = pl

                    if avg_pl > opt:
                        opt_signal = signal
                        opt = avg_pl
                        t1 = i
                        t2 = j

        return t1, t2, opt_signal
    except Exception as e:
        print(e)


def aroon_optimizer(price):
    """
    Pass a list of prices (or even an array)

    returns : a tuple of t1, and the optimal signal (t1 is optimal time period)
    """
    try:
        opt = -np.inf
        for i in range(1, 100):
            up, down = aroon_indicator(price, {'lb': i})

            signal = get_strategy_aroon(up, down)

            pl, _, _ = agg_pl_max_dd(signal, price)

            avg_pl = pl

            if avg_pl > opt:
                opt_signal = signal
                opt = avg_pl
                t1 = i

        return t1, opt_signal
    except Exception as e:
        print(e)


def bollinger_optimizer(prices):
    """
    Pass a list of prices (or even an array)

    returns : a tuple of t1, and the optimal signal (t1 is optimal time period)
    """
    try:
        opt = -np.inf
        for i in range(1, 200):
            up, down, price = get_bollinger_bands(prices, {'rate': i})

            signal = signal_strategy_bollb(up, down, price)

            pl, _, _ = agg_pl_max_dd(signal, prices)

            avg_pl = pl

            if avg_pl > opt:
                opt_signal = signal
                opt = avg_pl
                t1 = i

        return t1, opt_signal
    except Exception as e:
        print(e)


def gods_signal(price):
    """
    pass a list or an array of prices.

    outputs: god signal

    God Signal is the desired or the ultimate signal , the position one would take 
    if they come to know about the price tomorrow.
    """
    try:
        price = pd.Series(price)
        god_signal = np.sign(price.diff())
        return np.nan_to_num(god_signal)

    except Exception as e:
        print(e)
