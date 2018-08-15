""" 2018 Spring- ML4T-manual_strategy
Indicators.py implements my indicators as fucntions that operate on dataframes.
Generates the charts that illustrate the indicators for the report.
"""

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data, plot_data


def calculate_indicators (symbols = ['JPM'], sd = dt.datetime(2008,01,01), ed = dt.datetime(2009,12,31), window_size=20, plot_fig = True):
    
    #get prices table
    symbol = symbols[0]
    dates = pd.date_range(sd,ed)
    prices_all = get_data(symbols,dates)
    #fill up nan data
    prices_all.fillna(method='ffill',inplace = True)
    prices_all.fillna(method = 'bfill',inplace=True)
    #normalized prices
    prices_norm = prices_all/ prices_all.ix[0,:]

    price_SPY = prices_norm['SPY'] # only SPY price
    prices = prices_norm[symbols] # only portfolio

    #set the rolling days
    window_size = 20

    #for SMA
    sma = calculate_sma(prices, window_size)
    prices_sma = pd.DataFrame(0, index = prices.index, columns = ['price/SMA'])
    prices_sma['price/SMA'] = prices[symbol]/sma['SMA']

    #for bb
    bb = calculate_bollinger_bands(prices, window_size, sma)

    #for momentum
    mm = calculate_momentum(prices, window_size)


    #plot SMA, bb and momentum
    if plot_fig:
        sma_df = pd.concat([prices,sma,prices_sma],axis=1)
        sma_df.columns = [symbol, 'SMA','price/SMA']
#    print sma_df[0,:]
        ax1 = sma_df.plot(title = 'SMA indicator', grid = True, use_index = True)
        ax1.set_ylabel("normalized prices")
        ax1.set_xlabel("Date")
#    savefig("sma.png")

        bb_df = pd.concat([prices,bb['lower'],bb['upper'],sma],axis = 1)
        bb_df.columns = [symbol, 'Lower band', 'Upper band', 'SMA']
        ax2 = bb_df.plot(title = 'Bollinger Bands indicator', grid = True, use_index = True)
        ax2.set_ylabel("normalized prices")
        ax2.set_xlabel("Date")
#    savefig("bb.png")

        mm_df = pd.concat([prices, mm],axis = 1)
        ax3 = mm_df.plot(title = 'Momentum indicator', grid = True, use_index = True)
        ax3.set_ylabel("normalized prices")
        ax3.set_xlabel("Date")
#    xticks(np.arange(9), ('2008-01', '2008-04', '2008-07', '2008-10', '2009-01','2009'))
#    savefig("mm.png")
        plt.show()

def calculate_sma(prices, window_size):
    sma = pd.DataFrame(0, index = prices.index, columns = ['SMA'])
    sma['SMA'] = prices.rolling(window = window_size, min_periods = window_size).mean()
    return sma

def calculate_bollinger_bands(prices, window_size, sma):
    bb = pd.DataFrame(0, index = prices.index, columns = ['lower','upper'])
    bb_std = pd.DataFrame(0, index = prices.index, columns = ['std'])
    bb_std['std'] = prices.rolling(window = window_size, min_periods = window_size).std()
    rolling_mean = sma['SMA']
    bb['upper'] = rolling_mean + (bb_std['std'] *2)
    bb['lower'] = rolling_mean - (bb_std['std'] *2)
    return bb

def calculate_momentum(prices, window_size):
    mm = pd.DataFrame(0, index = prices.index, columns = ['Momentum'])
    mm['Momentum'] = prices.diff(window_size)/prices.shift(window_size)
    return mm

def test_code():
    calculate_indicators()

if __name__ == '__main__':
#    syms = ['JPM'],sd = dt.date(2008,1,1),ed = dt.date(2009,12,31))
    test_code()
