from datetime import datetime
from datetime import timedelta

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

