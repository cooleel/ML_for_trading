"""
StrategyLearner-Experiment1
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
#import StrategyLearner1 as sl1
import matplotlib.pyplot as plt


def print_info(portvals):
#    portvals = portvals / portvals.ix[0]
    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]

    print 'cumulative return: ' + str(float(portvals.values[-1] / portvals.values[0]) - 1)
    print 'Stdev of daily returns: ' + str(float(daily_returns.std()))
    print 'Mean of daily returns: ' + str(float(daily_returns.mean()))


if __name__== "__main__":
    #symbol used in experiment1
    symbol = 'JPM'
    #start date and end date for experiment1
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    dates = pd.date_range(sd,ed)
    #import all prices with SPY
    prices_all = ut.get_data([symbol],dates)
    #only prices in symbol
    prices = prices_all[symbol]

    #benchmark portvals table
    trades_benchmark = prices_all[[symbol,]].copy(deep=True)
    #benchmark buy and hold
    trades_benchmark.values[:, :] = 0
    trades_benchmark.values[0, :] = 1000
    vals_benchmark = marketsim(trades_benchmark, prices)#default impact and commission are 0

    #ML portvals table
    rtl = sl.StrategyLearner(verbose = False, impact = 0)
    #train learner
    rtl.addEvidence(symbol = symbol, sd = sd, ed = ed, sv = 100000)
    #testing
    trades_rtl = rtl.testPolicy(symbol = symbol,sd = sd, ed = ed, sv = 100000)
    vals_rtl = marketsim(trades_rtl, prices) #default impact and commission are 0

    #ML_3indicators portvals table
#    rtl3 = sl1.StrategyLearner(verbose = False, impact = 0)
    #train learner
#    rtl3.addEvidence(symbol = symbol, sd = sd, ed = ed, sv = 100000)
    #testing
#    trades_rtl3 = rtl3.testPolicy(symbol = symbol,sd = sd, ed = ed, sv = 100000)
#    vals_rtl3 = marketsim(trades_rtl3, prices) #default impact and commission are 0

    #manual_strategy portvals table
    trades_manual = manu.testPolicy(symbol = symbol, sd = sd, ed = ed)
    vals_manual = marketsim(trades_manual, prices)#default impact and commission are 0

    #normalization of the portvals
    vals_benchmark = vals_benchmark / vals_benchmark.ix[0]
    vals_rtl = vals_rtl / vals_rtl.ix[0]
#    vals_rtl3 = vals_rtl3 / vals_rtl3.ix[0]
    vals_manual = vals_manual / vals_manual.ix[0]

    #plots
    benchmark, = plt.plot(vals_benchmark, "b", label = "Benchmark")
    rtl, = plt.plot(vals_rtl, "r", label = "RTLearner_Strategy")
#    rtl3, = plt.plot(vals_rtl3, "g", label = "RTLearner_Strategy_3int")
    manual_strategy, = plt.plot(vals_manual, "k", label = "Manual_Strategy")
    plt.gcf().subplots_adjust(bottom= 0.2)
    plt.legend(handles =[benchmark,manual_strategy,rtl], loc=2)
#    plt.legend(handles =[benchmark,manual_strategy,rtl,rtl3], loc=2)
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.xticks(rotation = 45)
    plt.title("RTLearner VS Manual Strategy")

    plt.show()
