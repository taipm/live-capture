from datetime import date
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd


#2022-10-14
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



TODAY = date.today()
fmt_day = '%Y-%-m-%d'
StrTODAY = TODAY.strftime(fmt_day)

YESTERDAY = TODAY - timedelta(days=1)
StrYESTERDAY = YESTERDAY.strftime(fmt_day)
NOW = datetime.now()

THIS_YEAR = datetime.now().year
THIS_MONTH = datetime.now().month
THIS_DAY = TODAY.day
#print(THIS_DAY)

#FIRST_DAY_OF_YEAR = date(THIS_YEAR,1,1)
#LAST_DAY_OF_YEAR = date(THIS_YEAR,12,31)


def Is_Business_Day(date):
    return bool(len(pd.bdate_range(date, date)))
    
def compareDates(dt1, dt2):
    pass

def percent(x,y):
    if(y !=0):
        return ((x-y)/y)*100
    return None

# def Text_To_Markdown2(text):
#     return text
#         .replace('/\_/g, '\\_')
#         .replace(/\*/g, '\\*')
#         .replace(/\[/g, '\\[')
#         .replace(/\]/g, '\\]')
#         .replace(/\(/g, '\\(')
#         .replace(/\)/g, '\\)')
#         .replace(/\~/g, '\\~')
#         .replace(/\`/g, '\\`')
#         .replace(/\>/g, '\\>')
#         .replace(/\#/g, '\\#')
#         .replace(/\+/g, '\\+')
#         .replace(/\-/g, '\\-')
#         .replace(/\=/g, '\\=')
#         .replace(/\|/g, '\\|')
#         .replace(/\{/g, '\\{')
#         .replace(/\}/g, '\\}')
#         .replace(/\./g, '\\.')
#         .replace(/\!/g, '\\!')
