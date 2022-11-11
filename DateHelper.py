from datetime import date
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd

def parse_text_to_date(str_date):
    if('-' in str_date):
        return datetime.strptime(str_date, '%Y-%m-%d').date()
    else:
        return None

def get_next_date(str_date, days):
    date = parse_text_to_date(str_date=str_date)
    next_date = date + timedelta(days=days)
    return next_date

def get_after_date(str_date):
    date = parse_text_to_date(str_date=str_date)
    next_date = date + timedelta(days=1)
    return next_date

def get_prev_date(str_date):
    date = parse_text_to_date(str_date=str_date)
    next_date = date - timedelta(days=1)
    return next_date

#NUMBER
billion = 1000000000 #Tỷ
million = 1000000

#TIME
NOW = datetime.now()
TODAY = date.today()
fmt_day = '%Y-%-m-%d'
StrTODAY = TODAY.strftime(fmt_day)

YESTERDAY = TODAY - timedelta(days=1)
StrYESTERDAY = YESTERDAY.strftime(fmt_day)
NOW = datetime.now()

THIS_YEAR = datetime.now().year
THIS_MONTH = datetime.now().month
THIS_DAY = TODAY.day

def Is_Business_Day(date):
    return bool(len(pd.bdate_range(date, date)))
    
def inc_percent(x, p):
    '''
    p: Phần trăm (nếu 3% thì p = 3)
    '''
    return x + (p/100)*x

def percent(x,y):
    if(x !=0):
        return ((x-y)/x)*100
    return None

def profit(mua, ban):
    if(mua != 0):
        return ((ban-mua)/mua)*100
    else:
        return None

#print(profit(1,2))