import datetime
from time import sleep
from RSI import relative_strength
import matplotlib.pyplot as plt
import pandas as pd    
import io
#import numpy as np
#import pandas as pd
#import mplfinance as mpf
#import matplotlib.pyplot as plt
from vnstock import *
import pandas as pd
#import matplotlib.pyplot as plt
import io
import mplfinance as mpf
#import pandas as pd
import matplotlib.pyplot as plt

def plot_candlestick_chart(symbol, start_date, end_date):
    df = stock_historical_data(symbol=symbol, start_date=start_date, end_date=end_date)
    df['Date'] = df['TradingDate']
    del df['TradingDate']
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Tính toán đường EMA21
    ema21 = df['Close'].ewm(span=21, adjust=False).mean()
    apd_ema21 = mpf.make_addplot(ema21, color='red', title = 'EMA21')
    
    df['rsi'] = relative_strength(df['Close'], n=7)    
    apd_rsi = mpf.make_addplot(df['rsi'],panel=2,color='lime',ylim=(10,90),secondary_y=True)
    
    # Thêm đường EMA21 vào đồ thị
    mpf.plot(df, type='candle', volume=True, style='yahoo', mav=(10, 20), figscale=1.5, addplot=[apd_ema21, apd_rsi], panel_ratios=(1, 0.6),title=f'{symbol}, {end_date}')
    
    # Thêm ghi chú "EMA21" vào đồ thị
    
    # plt.title(symbol)
    #plt.legend()


    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer

# today_str = datetime.now().strftime("%Y-%m-%d")
# plot_candlestick_chart(symbol='ASM',start_date='2022-06-01',end_date=today_str)  

