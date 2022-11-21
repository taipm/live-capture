from datetime import date
from datetime import datetime
from datetime import timedelta
import pandas as pd
import datetime

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

def isToday(text):
    '''
    fomart: '2022-11-17 06:48:05.904288'
    '''
    date_time_obj = datetime.datetime.strptime(text, '%Y-%m-%d %H:%M:%S.%f')
    _date = date_time_obj.date()
    today= datetime.datetime.now().date()

    if(_date == today):
        return True
    else:
        return False

#TIME
NOW = datetime.datetime.now()
TODAY = date.today()
fmt_day = '%Y-%-m-%d'
StrTODAY = TODAY.strftime(fmt_day)

YESTERDAY = TODAY - timedelta(days=1)
StrYESTERDAY = YESTERDAY.strftime(fmt_day)

def Is_Business_Day(Adate):
    return bool(len(pd.bdate_range(date, date)))


#print(profit(1,2))