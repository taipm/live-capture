from datetime import date
from datetime import datetime
from datetime import timedelta
import datetime

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