"""Seattle University, OMSBA 5062, DTC, Jomaica Lei

Functions:
recession_visual - plots a graphic visual showing the inverted yield curve
print_correlation - prints comparable correlations of price data
"""
import os
import csv
import matplotlib.pyplot as plt
import scipy
from scipy.stats import pearsonr
from datetime import datetime
from p2_TimeSeries import TimeSeries, Fred, dgs3mo, dgs10, Bundesbank, gold_spot, Difference, lag, returns

DATA = '/Users/jomaicaalfiler/Desktop/MSBA/Python - 5062/Week 7/DTC/'

def print_correlations():
    """This function compute correlations between 
    the difference of treasury assets paired with gold prices, 
    and gold prices along with a lagged selling profit in the TimeSeries file.
    """
    short = dgs3mo()
    long = dgs10()
    gold = gold_spot()
    dates = short.get_dates()
    dates = long.get_dates(dates)  
    diff = long - short
    gold_correlation, pval = gold.correlation(diff)
    print('Correlation between dgs10-dgs3mo and gold_spot: {:.2%}'.format(gold_correlation))
    buy_lag = 3  
    hold_time = 20  
    investment = returns(gold, hold_time)  
    signal = diff  
    compare_to = lag(signal, buy_lag + hold_time)  
    signal_to_result_correlation, pval = investment.correlation(compare_to)
    print("Correlation between dgs10-dgs3mo and gold returns (" + str(buy_lag) +
          " days wait, " + str(hold_time) + " day hold): {:.2%}".format(
        signal_to_result_correlation))  


def recession_visual():
    """Data visualization of the inverted yield curve for the treasurey assets vs. gold price."""
    short = dgs3mo()
    long = dgs10()
    gold = gold_spot()
    dates = short.get_dates()
    dates = long.get_dates(dates)  
    gold_date = gold.get_dates(dates)
    gold_val = gold.get_values(dates)
    diff = long - short
    y_diff = diff.get_values(dates)
    x_dates = diff.get_dates(candidates=dates)

    fig = plt.figure(1)
    ax = fig.add_subplot(111) 
    left = ax.plot(gold_date, gold_val, color='orange')
    ax.set_ylabel('USD per ounce')
    ax.set_xlabel('date')
    axr = ax.twinx() 
    right = axr.plot(x_dates, y_diff)
    axr.set_ylabel('percent per anum')  
    axr.axhline(y=0, color='r')
    fig.autofmt_xdate()  
    ax.legend(left + right, ['gold_spot', 'dgs10-dgs3mo'],
              loc='upper center')
    ax.set_title('Gold vs. Yield Curve Inversion')
    plt.show()


if __name__ == '__main__':
    print_correlations()
    recession_visual()