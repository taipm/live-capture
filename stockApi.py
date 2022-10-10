import pandas as pd
import numpy as np
import datetime
from urllib.request import urlopen, Request
import db
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def GetMarketPrice(symbol):
  market_price = db.get_stock_data_from_api(symbol=symbol).iloc[0]['Close']

def GetSticks_Intraday(symbol):
  url = f'https://s.cafef.vn/Lich-su-giao-dich-{symbol}-6.chn#data'
  data = pd.read_html(url)
  
  df_sticks = data[len(data)-1]
  df_sticks = pd.DataFrame(df_sticks.values,columns=['Time','PriceX','Volume','Sum Volume','Percent'])

  #Tách giá
  df_sticks['Price'] = df_sticks['PriceX'].apply(lambda x: x.split(' ')[0])
  df_sticks['Price']

  df_sticks['%'] = df_sticks['PriceX'].apply(lambda x: x.split(' ')[2])
  df_sticks['%'] = df_sticks['%'].apply(lambda x: x[1:len(x)-2])

  del df_sticks['PriceX']

  #cols = ['Volume','Sum Volume','Price','%','Percent']
  cols = ['Volume','Sum Volume','Price','%']
  df_sticks[cols] = df_sticks[cols].apply(pd.to_numeric, downcast='float', errors='coerce')



  df_sticks['Time'] = df_sticks['Time'].apply(lambda x: datetime.datetime.today().strftime('%Y-%m-%d') + ' ' + str(x))
  df_sticks['Time'] = df_sticks['Time'].astype("datetime64")
  df_sticks.set_index('Time')

  df_sticks['Money'] = df_sticks['Price']*df_sticks['Volume']

  return df_sticks

# symbol = 'VND'
# df_sticks = GetSticks_Intraday(symbol=symbol)
# print(df_sticks)
def getMaxStickVolume(stock):
  df = GetSticks_Intraday(symbol=stock)
  max_volume = df['Volume'].max()
  item = df[df['Volume']==max_volume]
  return item

def analysisOrderSticks(df):
  output = ''
  output += output
  return output


# stock = 'VND'
# df = GetSticks_Intraday(symbol=stock)
# max_volume = getMaxStickVolume(df)
# print(max_volume)