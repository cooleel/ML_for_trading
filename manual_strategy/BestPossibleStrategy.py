""" 2018 Spring- ML4T-manual_strategy
Code implementing a BestPossibleStrategy object.
It should implement testPolicy() which returns a trades data frame (see below).
The main part of this code should call marketsimcode as necessary to generate the plots used in the report.
"""

import numpy as np
import pandas as pd
import datetime as dt
import os
import math
import types
from marketsimcode import marketsim
import matplotlib.pyplot as plt
from util import get_data, plot_data

def testPolicy(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]
    trades_df = pd.DataFrame(data=np.zeros(len(prices.index)), index=prices.index, columns = ['val'])
    value = prices.values

    # Calculate the first day
    price_up = value[1] > value[0]
    trades_df['val'].iloc[0] = 1000 * (1 if price_up else -1)

    # Check the prices one day after, compare to today's price

    for i in range(1, len(value) - 1):
        if (value[i] < value[i + 1] and not price_up) or (value[i] >= value[i + 1] and price_up):
            price_up = not price_up
            trades_df['val'].iloc[i] = 2000 * (1 if price_up else -1)

    return trades_df

def print_info(portvals):
    portvals = portvals / portvals.ix[0]
    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]

    print 'cumulative return: ' + str(float(portvals.values[-1] / portvals.values[0]) - 1)
    print 'Stdev of daily returns: ' + str(float(daily_returns.std()))
    print 'Mean of daily returns: ' + str(float(daily_returns.mean()))

if __name__ == '__main__':
    names = ['JPM']
    start_date = '2008-01-01'
    end_date = '2009-12-31'
    prices = get_data(names, pd.date_range(start_date, end_date))
    prices = prices[names]

    trades_df = testPolicy()
    portvals = marketsim(trades_df, prices)
    print 'Best Possible Policy performance'
    print_info(portvals)

    d = np.zeros(len(prices.index))
    d[0] = 1000
    trade_df_none = pd.DataFrame(data=d, index=prices.index, columns = ['val'])
    port_benchmark = marketsim(trade_df_none, prices)
    print 'Benchmark performance'
    print_info(port_benchmark)

    #normalization the portvals
    portvals = portvals / portvals.ix[0]
    port_benchmark = port_benchmark / port_benchmark.ix[0]

    # plot the graph
    plt.gcf().subplots_adjust(bottom= 0.2)
    benchmark, = plt.plot(port_benchmark, 'b')
    best, = plt.plot(portvals, 'k')

    plt.legend([benchmark, best], ['Benchmark', 'Best_Port'],loc='upper left')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.xticks(rotation = 45)
    plt.title("BestPossibleStrategy VS Benchmark")
    plt.show()
