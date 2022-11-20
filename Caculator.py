from math import *
import numpy as np

def EvaluationOrder(old_vol, old_price, market_price, ratio_profit):
    print(f'{old_vol} {old_price} {market_price} {ratio_profit}')
    new_vol = ((market_price*(1-ratio_profit))*old_vol - old_price*old_vol)/(ratio_profit*market_price)
    new_vol = trunc(new_vol)
    return new_vol