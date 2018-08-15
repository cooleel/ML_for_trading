""" 2018 Spring- ML4T-manual_strategy
An imporved version of my marketsim code that accepts a "trades" data frame
Shanshan Wang
swang637
"""

import numpy as np
import pandas as pd
import datetime as dt
import math
import os
import types
import matplotlib.pyplot as plt
from util import get_data, plot_data

# an improved version of marketsim, generate the portfolio values
# holding table and price table
def marketsim(trades_df, prices, sv=100000, sh = 0, commission = 0, impact = 0):
    # generate the holding table
    holding_df = pd.DataFrame(data=np.ones(len(prices)) * sh, index=prices.index, columns=['val'])
    # generate the cash table
    cash_df = pd.DataFrame(data=np.ones(len(prices)) * sv, index=prices.index, columns=['val'])
    for i in range(len(prices.index)):
        cash_change = 0

        # signal = 1 lead to buy, signal = -1 lead to sell
        signal = 1 if trades_df.values[i][0] > 0 else -1

        if trades_df.values[i][0] != 0:
            cash_change = (signal + impact) * abs(trades_df.values[i][0]) * prices.values[i]
            cash_change += commission
        if i == 0:
            cash_df['val'].iloc[i] -= cash_change
            holding_df['val'].iloc[i] += trades_df.values[i][0]
            continue
        cash_df['val'].iloc[i] = cash_df['val'].iloc[i - 1] - cash_change
        holding_df['val'].iloc[i] = holding_df['val'].iloc[i - 1] + trades_df.values[i][0]

    # dataframe for share value equals holdings * prices
    share_df_val = holding_df.val * prices
    portvals = share_df_val + cash_df.val
    return portvals

if __name__ == "__main__":
    syms = ['JPM']
    start_date = '2008-01-01'
    end_date = '2009-12-31'
    prices = get_data(syms, pd.date_range(start_date, end_date))
    prices = prices[syms]
    trades_df = pd.DataFrame(data=np.random.randint(-1, 2, size=len(prices.index))*1000, index=prices.index, columns = ['val'])
    portvals = marketsim(trades_df, prices)
    print portvals
