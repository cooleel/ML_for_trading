"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
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
import math

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        # according to RTLearner bagging condition
        self.learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":5}, bags = 20)
        self.window_size = 20
        self.idt_size = 5
        self.N = 10

    # Use bagged RTLearner to build this trader
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        window_size = self.window_size
        idt_size = self.idt_size
        #Check for N day return
        N = self.N

        threshold = max(0.03, 2 *self.impact)
        #check indicators
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices = prices[symbol]
        SMA = manu.simple_moving_average(prices,window_size = 20)
#        sma_int = prices[symbol]/SMA['SMA']-1
#        BB = manu.bollinger_band(prices,window_size=20)
#        MM = manu.momentum(prices,window_size = 20)
#        MM = idt.calculate_indicators(symbols=[symbol],sd=sd,ed=ed,window_size=self.window_size,plot_fig=False)
        #turn regression model to Classification
        X= []
        Y= []
        for i in range(window_size + idt_size + 1, len(prices)-N):
            X.append(np.array(SMA[i-idt_size:i]))
#            X.append(np.array(SMA[i-idt_size:i]))
            gain = (prices.values[i+N] - prices.values[i])/prices.values[i]
            if gain > threshold:
                Y.append(1)
            elif gain < -threshold:
                Y.append(-1)
            else:
                Y.append(0)

        X =np.array(X)
        Y =np.array(Y)

        self.learner.addEvidence(X,Y)
    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        current_holding = 0
        dates = pd.date_range(sd,ed)
        prices_all = ut.get_data([symbol],dates)
        trades = prices_all[[symbol,]].copy(deep=True)
        trades_SPY = prices_all['SPY']

        window_size = self.window_size
        idt_size = self.idt_size
        #check indicators
        #SMA,BB,MM = idt.calculate_indicators(symbols=[symbol],sd=sd,ed=ed,window_size=self.window_size,plot_fig=False)
        #check indicators
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices = prices[symbol]
        SMA = manu.simple_moving_average(prices,window_size = 20)
#        sma_int = prices[symbol]/SMA['SMA']-1
#        BB = manu.bollinger_band(prices,window_size=20)

#        MM = manu.momentum(prices,window_size = 20)
        trades.values[:,:] = 0
        Xtest = []
#        prices = prices_all[symbol]
        for i in range(window_size + idt_size +1, len(prices)-1):
            data = np.array(SMA[i-idt_size:i])
            #data = np.array(SMA[i-idt_size:i])
            Xtest.append(data)

        result= self.learner.query(Xtest)
        for i,r in enumerate(result):
            if r > 0:
                trades.values[i + window_size + idt_size +1,:] = 1000- current_holding
                current_holding = 1000
            elif r < 0:
                trades.values[ i + window_size + idt_size +1,:] = -1000 - current_holding
                current_holding = -1000
#        if self.verbose: print type(trades)
#        if self.verbose: print trades
#        if self.verbose: print prices_all

        return trades

    def author():
        return "swang637"

if __name__=="__main__":
    print "One does not simply think up a strategy"
