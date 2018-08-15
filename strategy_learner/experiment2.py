"""
StrategyLearner-Experiment2
Shanshan Wang
swang637
"""

import datetime as dt
import pandas as pd
import numpy as np
import util as ut
import random
import BagLearner as bl
import RTLearner as rt
import indicators as idt
import ManualStrategy as manu
from marketsimcode import marketsim
import StrategyLearner as sl
import matplotlib.pyplot as plt


def print_info(portvals):
#    portvals = portvals / portvals.ix[0]
    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]

    print 'cumulative return: ' + str(float(portvals.values[-1] / portvals.values[0]) - 1)
    print 'Stdev of daily returns: ' + str(float(daily_returns.std()))
    print 'Mean of daily returns: ' + str(float(daily_returns.mean()))

if __name__ == '__main__':
    symbol = 'JPM'
    # sd = datetime.datetime(2010, 1, 1)
    # ed = datetime.datetime(2011, 12, 31)
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    prices = ut.get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]

    res = []
    trades_num = []
    impacts = [0, 0.025, 0.05, 0.1, 0.2, 0.4]
    for impact in impacts:
        learner = sl.StrategyLearner(verbose = False, impact = impact)
        # constructor
        #training the learner
        learner.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = 100000)
        #testing Period
        trades_df = learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = 100000)
        trades_num.append(np.count_nonzero(trades_df))

        vals_rtl = marketsim(trades_df, prices, impact = impact)

        vals_rtl = vals_rtl / vals_rtl.ix[0]
        print_info(vals_rtl)
        print trades_num
        res.append(vals_rtl)


    plt.xlabel('impact')
    plt.ylim(ymax = 60)
    plt.ylabel('number of trades')
    plt.xticks(np.arange(6), impacts)
    plt.plot(trades_num)
    plt.title("Impact on number of trades")
    plt.show()

    handles = []
    for i in range(len(impacts)):
        rtlstrategy, = plt.plot(res[i], label = str(impacts[i]))
        handles.append(rtlstrategy)

    plt.gcf().subplots_adjust(bottom= 0.2)
    plt.legend(handles=handles, loc=2)
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.xticks(rotation = 45)
    plt.title("RTLearner with different impacts")
    plt.show()
