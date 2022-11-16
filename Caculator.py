from math import *
import numpy as np
from Parameters import *

def EvaluationOrder(old_vol, old_price, market_price, ratio_profit):
    print(f'{old_vol} {old_price} {market_price} {ratio_profit}')
    new_vol = ((market_price*(1-ratio_profit))*old_vol - old_price*old_vol)/(ratio_profit*market_price)
    new_vol = trunc(new_vol)
    return new_vol

def test_evaluationOder():
    stock = 'HPG'
    old_vol = 200
    market_price = 17.6
    old_price = 22.275
    ratio = -5/100

    new_vol = EvaluationOrder(old_vol=old_vol, old_price=old_price,ratio_profit=ratio,market_price=market_price)
    print(new_vol)

    p_avg = (old_price*old_vol + new_vol*market_price)/(new_vol+old_vol)
    ratio_profit = (market_price-p_avg)/p_avg

    print(f'Gia TB : {p_avg} - LN: {ratio_profit}')

    if(ratio_profit >= ratio):
        print('Tính toán đúng')
    else:
        print('Tính toán sai')

#test_evaluationOder()dad
def split_array(arr, sizeOf_item = 5): #SAI, ĐANG CHIA 05 PHẦN
    return np.array_split(arr, sizeOf_item)

