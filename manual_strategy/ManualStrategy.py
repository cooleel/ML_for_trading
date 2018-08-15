""" 2018 Spring- ML4T-manual_strategy
Code implementing a ManualStrategy object.
It should implement testPolicy() which returns a trades data frame (see below).
The main part of this code should call marketsimcode as necessary to generate
the plots used in the report.
"""

import numpy as np
import pandas as pd
import datetime as dt
import math
import types
import os
import matplotlib.pyplot as plt
from marketsimcode import marketsim
from util import get_data, plot_data
#from indicators import calculate_sma,calculate_bollinger_bands,calculate_momentum

# generate a moving average
def moving_average(vals, window_size = 20):
    value = np.cumsum(vals, dtype = float)
    value[window_size :] = value[window_size :] - value[: -window_size]
    return value[window_size - 1 : -1] / window_size

#generate sma indicator
def simple_moving_average(prices, window_size = 20):
    prices = prices / prices.ix[0]
    price_val = np.array(prices.values)
    moving_avg = np.concatenate((np.array([np.nan] * (window_size)), moving_average(price_val, window_size = window_size)))
    df_moving_avg = pd.DataFrame(data=moving_avg, index=prices.index, columns=['val'])
    sma_in = price_val / moving_avg - 1
    return sma_in

   # printout the profolio values information
def print_info(portvals):
    portvals = portvals / portvals.ix[0]
    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]

    print 'cumulative return: ' + str(float(portvals.values[-1] / portvals.values[0]) - 1)
    print 'Stdev of daily returns: ' + str(float(daily_returns.std()))
    print 'Mean of daily returns: ' + str(float(daily_returns.mean()))


def testPolicy(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]
    df_trades = pd.DataFrame(data=np.zeros(len(prices.index)), index=prices.index, columns = ['val'])
    # initial the holding table
    current = 0
    window_n = 20

    SMA = simple_moving_average(prices,window_size = window_n)


    # Manual Strategy using Simple Moving Average,
    # check different window sizes

    for i in range(window_n, len(prices.index)):
        # the threshold here is 0.1
        # Smaller than threshold -> buy
        # Bigger than threshold -> sell
        if SMA[i] < -0.1:
            df_trades['val'].iloc[i] = 1000 - current
            current = 1000
        elif SMA[i] > 0.1:
            df_trades['val'].iloc[i] = - current - 1000
            current = -1000

    return df_trades

if __name__ == '__main__':
    syms = ['JPM']
    start_date = '2008-01-01'
    end_date = '2009-12-31'
    #for out-sample time using following sd and ed
    #start_date = '2010-01-01'
    #end_date = '2011-12-31'
    prices = get_data(syms, pd.date_range(start_date, end_date))
    prices = prices[syms]
    # print prices
    df_trades = testPolicy(sd=start_date, ed=end_date)
    df_joined = df_trades.join(prices, lsuffix='_best', rsuffix='_benchmark')

    portvals = marketsim(df_trades, prices, commission = 9.95, impact = 0.005)
    # portvals = marketsim(df_trades, prices, commission = 0, impact = 0)
    df_joined = df_joined.join(portvals, lsuffix='_best', rsuffix = 'whatever')
    prices_val = prices.values

    # to generate Benchmark values
    d = np.zeros(len(prices.index))
    d[0] = 1000
    df_trade_none = pd.DataFrame(data=d, index=prices.index, columns = ['val'])
    port_benchmark = marketsim(df_trade_none, prices)

    portvals = portvals / portvals.ix[0]
    port_benchmark = port_benchmark / port_benchmark.ix[0]

    print "My strategy performance"
    print_info(portvals)
    print "Benchmark performance"
    print_info(port_benchmark)


    benchmark, = plt.plot(port_benchmark, 'b')
    mystrategy, = plt.plot(portvals, 'k')
    for i in range(len(prices.index)):
        if df_trades['val'].iloc[i] > 0:
            plt.axvline(x=prices.index[i], c = 'g')
        elif df_trades['val'].iloc[i] < 0:
            plt.axvline(x=prices.index[i], c = 'r')
#generate the graphs
    plt.gcf().subplots_adjust(bottom= 0.2)
    plt.legend([benchmark, mystrategy], ['Benchmark', 'My Strategy'],loc='upper right')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.xticks(rotation = 45)
    plt.title("My Strategy VS Benchmark (Development Period)")
    plt.show()



"""    sma = pd.DataFrame(0, index = prices.index, columns = ['SMA'])
    sma['SMA'] = prices.rolling(window = my_window, min_periods = my_window).mean()
#    sma = calculate_sma(prices, window_size = my_window)
    prices_sma = pd.DataFrame(0, index = prices.index, columns = ['price/SMA'])
    prices_sma['price/SMA'] = prices[symbol]/sma['SMA']-1
    SMA = prices_sma['price/SMA']
#    BB = calculate_bollinger_bands(prices, window = my_window, SMA)
#    MM = calculate_momentum(prices, window_size = my_window)
"""
