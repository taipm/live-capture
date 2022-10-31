import pandas as pd
import numpy as np
import datetime
from urllib.request import urlopen, Request
import db
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from vnstock import *


STOCKS = ['HPG', 'VND', 'DPM', 'FRT']
STOCKS = ','.join(map(str, STOCKS))

# board = price_board(STOCKS)
# print(board.transpose())

# print(type(board))
# print(board)

# stock = board.iloc[0]
# print(stock)