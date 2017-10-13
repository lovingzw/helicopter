#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:27:48 2017

@author: MAngO
"""

import numpy as np

def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):
    ''' Write your own strategy here in the strategy function

    Params: timer = int, counter of current time
            data = pandas.dataframe, data for current minute bar
            info - pandas.dataframe, information matrix
            init_cash，transaction - double, constans
            detail_last_min - list, contains cash balance, margin balance, total balance and position of last minute
            memory - class, current memory of your strategy
    
    You are allowed to access the data(open, high, low, close, volume) of current minute,
    the current time, initial settings(initial cash and transaction cost).
    
    Notes:
    1. All data else you need in your model and strategy should be stored by yourself in 
    memory variable.
    
    2. Return value are limited to be in the following form: position_matrix_of_next_minute, 
    memory_list
    
    3. Backtest module will accept return values from your strategy function and use them as
    new input into your strateg function in next minute.
    
    4. Strategy functions that cannot operate properly in back test may ower your final grade.
    Please double check to make sure that your strategy function satisfy all the requirments above.
    '''

    ''' Testing strategy that buy and hold, always hold AU futures contract with half of your capital
    '''
    index = 2 # i.e. AU.SHF, here index is 2 because index of python list starts from 0
    
    position = np.repeat(0.,data.shape[0])

    buy(position,index,0.5*init_cash,data,info,transaction)
    
    # This simple strategy doesn't need any memory parameters, so we just return empty list 
    return position,memory

def train(*args, **kwargs):
    ''' If your strategy needs training process, please write training function here and run it in main 
    '''
    pass


if __name__ == '__main__':
    pass

''' add auxiliary fucntion hear
'''
def buy(position, index, amount_cash, data, info, transaction):
    """
    Buy certain amount of lots for one future 
    :param position: list,current position
    :param index: int, one certain future index
    :param amount_cash: double, amount of cash to buy
    :param data: pandas.dataframe, data for current minute bar
    :param info: pandas.dataframe, information matrix
    :param transaction: double, transaction fee
    :return: returns nothing
    """
    # Get execution price of this minute
    avg_price = np.mean(data[index, :4])

    #Get the value of one lot so that you can get how many lots you can buy in total
    lot_value = avg_price * info.unit_per_lot[index] * info.margin_rate[index]

    position[index] = np.round(amount_cash / (lot_value * (1. + transaction)))

    return True


def sell(position,index):
    """
    Sell all lots for one future 
    :param position: list,current position
    :param index: int, one certain future index
    """
    position[index]=0