import pandas as pd
import matplotlib.pyplot as plt
import db


import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# load the stock price data into a pandas dataframe
#df = pd.read_csv("stock_data.csv")
data = db.GetStockData(symbol='VGI')
df = data.sort_values(by=['Date']).tail(50)
import pandas as pd
import numpy as np

def RSI(close, n=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(n).mean()
    avg_loss = loss.rolling(n).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = RSI(df['Close'])

import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Tạo figure với 3 subplots
fig = make_subplots(rows=3, cols=1, shared_xaxes=False)

# Thêm đồ thị Candlestick vào subplot 1
fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], close=df['Close'], high=df['High'], low=df['Low']))

# Thêm đồ thị khối lượng vào subplot 2
#fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name="Volume"))

# Thêm đồ thị RSI vào subplot 3
fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name="RSI"))

# Tạo layout cho figure
fig.update_layout(title="Candlestick, Volume and RSI")

# Hiển thị figure
fig.show()

