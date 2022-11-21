from math import *

def EvaluationOrder(old_vol, old_price, market_price, ratio_profit):
    print(f'{old_vol} {old_price} {market_price} {ratio_profit}')
    new_vol = ((market_price*(1-ratio_profit))*old_vol - old_price*old_vol)/(ratio_profit*market_price)
    new_vol = trunc(new_vol)
    return new_vol


def CompoundingInterest(amount, rate, rountines):
    amount = amount
    for i in range(0, rountines):
        amount += amount*rate
    return amount

# x = CompoundingInterest(amount=100000000, rate=3/100, rountines=10)
# print(f'{x:,.2f}')

def inc_percent(x, p):
    '''
    p: Phần trăm (nếu 3% thì p = 3)
    '''
    return x + (p/100)*x

def percent(x,y):
    if(x !=0):
        return ((y-x)/x)*100
    return None

def profit(mua, ban):
    if(mua != 0):
        return ((ban-mua)/mua)*100
    else:
        return None
