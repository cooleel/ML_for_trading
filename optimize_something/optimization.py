"""MC1-P2: Optimize a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as pro
from util import get_data, plot_data



def stat(allocs,prices):
    sv = 1000000.0
    rfr = 0.0
    sf = 252.0
#    normed_price = prices/prices.iloc[0,:]    #normalized price
    pos_vals = prices * allocs * sv #get each allocation
#    pos_vals = alloced_price * sv
    port_val = pos_vals.sum(axis=1)

    cr = (port_val[-1]/port_val[0])-1
    daily_rets = (port_val/port_val.shift(1))-1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    k = np.sqrt(sf)
    sr = k*np.mean((adr-rfr)/sddr)
    return [cr,adr,sddr,sr,port_val]

def min_fun_sddr(allocs,prices):
    return stat(allocs,prices)[2]


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    prices = prices/prices.iloc[0,:]
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
#    allocs = np.asarray([0.2, 0.2, 0.3, 0.3])


    n = len(syms)
    Xallocs = n*[1.0/n,]
#    Xallocs /=np.sum(Xallocs)# get the starting allocation
    cons = ({'type':'eq','fun':lambda x: np.sum(x) -1})
    bounds = tuple((0,1) for x in range(n))
    min_allocs = pro.minimize(min_fun_sddr,Xallocs,args = (prices,), method = 'SLSQP',bounds = bounds,constraints = cons)
    cr,adr,sddr,sr,port_val = stat(prices, min_allocs.x)
    allocs = min_allocs.x



    # add code here to find the allocations
#    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

    # Get daily portfolio value
#    port_val = prices_SPY # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp = df_temp / df_temp.ix[0,:]
        ax = df_temp.plot(title="Daily portfolio value and SPY")
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized price")
#        ax.xaxis.tick
        plt.savefig("MC1-P2.png")
#        plt.show()

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM','X','GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
