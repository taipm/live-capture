import pandas as pd
import requests
from pandas import json_normalize
from datetime import datetime
from datetime import timedelta
import time
from io import BytesIO
import openpyxl

# def get_intraday_data(symbol, page_num, page_size):
#     """
#     This function returns the stock realtime intraday data.
#     Args:
#         symbol (:obj:`str`, required): 3 digits name of the desired stock.
#         page_size (:obj:`int`, required): the number of rows in a page to be returned by this query, suggest to use 5000.
#         page_num (:obj:`str`, required): the page index starting from 0.
#     Returns:
#         :obj:`pandas.DataFrame`:
#         | tradingDate | open | high | low | close | volume |
#         | ----------- | ---- | ---- | --- | ----- | ------ |
#         | YYYY-mm-dd  | xxxx | xxxx | xxx | xxxxx | xxxxxx |
#     Raises:
#         ValueError: raised whenever any of the introduced arguments is not valid.
#     """
#     d = datetime.now()
#     if d.weekday() > 4: #today is weekend
#         data = requests.get('https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/{}/his/paging?page={}&size={}&headIndex=-1'.format(symbol, page_num, page_size)).json()
#     else: #today is weekday
#         data = requests.get('https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/{}/his/paging?page={}&size={}'.format(symbol, page_num, page_size)).json()
#     df = json_normalize(data['data']).rename(columns={'p':'price', 'v':'volume', 't': 'time'})
#     return df


# _page_num = 0
# _page_size = 5000
# x = get_intraday_data(symbol= 'HPG', page_num=_page_num,page_size=_page_size)
# print(x.head(10))