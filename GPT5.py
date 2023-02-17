#Darvas

import pprint
import pandas as pd
import numpy as np

def darvas_trading_strategy(data):
    data = data.copy()
    data["position"] = 0
    data["profit"] = 0
    data["cash"] = 100000
    data["shares"] = 0
    
    buy_price = 0
    for i in range(1, len(data)):
        if data.at[i, "Close"] > data.at[i-1, "Close"] and data.at[i, "High"] >= data.at[buy_price, "High"] if buy_price != 0 else True:
            if buy_price == 0:
                buy_price = i
            elif data.at[i, "Close"] > data.at[buy_price, "Close"]:
                data.at[buy_price, "position"] = -1
                data.at[i, "position"] = 1
                shares = data.at[buy_price, "cash"] / data.at[buy_price, "Close"]
                data.at[buy_price, "cash"] -= shares * data.at[buy_price, "Close"]
                data.at[buy_price, "shares"] = shares
                data.at[i, "cash"] = data.at[buy_price, "shares"] * data.at[i, "Close"]
                data.at[i, "shares"] = 0
                buy_price = 0
    
    data["profit"] = data["shares"] * data["Close"] + data["cash"]
    return data

def find_trades(data, box_size=20):
    """
    Hàm dùng thuật toán Darvas để tìm kiếm các vị trí lệnh mua/lệnh bán trong dữ liệu.

    data: pandas DataFrame chứa dữ liệu giá cổ phiếu
    box_size: kích thước hộp Darvas (mặc định là 20)

    Trả về:
    trades: một DataFrame chứa các giao dịch tìm được
    """
    trades = pd.DataFrame(columns=['Buy Date', 'Sell Date', 'Buy Price', 'Sell Price'])

    # Lặp qua từng giá cả cổ phiếu trong dữ liệu
    for i in range(len(data)):
        if i <= box_size:
            continue
        
        current_price = data.iloc[i]['Close']
        high = max(data.iloc[i-box_size:i]['High'])
        low = min(data.iloc[i-box_size:i]['Low'])
        
        if current_price == high:
            # Lệnh mua
            trades = trades.append({'Buy Date': data.iloc[i]['Date'],
                                    'Buy Price': current_price}, ignore_index=True)
            print(f"Buy {data.iloc[i]['Date']} - {current_price}")
        elif current_price == low:
            # Lệnh bán
            try:
                trades.at[trades.index[-1], 'Sell Date'] = data.iloc[i]['Date']
                trades.at[trades.index[-1], 'Sell Price'] = current_price
                print(f"Sell {data.iloc[i]['Date']} - {current_price}")
            except:
                print(f'Lỗi chưa bán được do chỉ số index[-1]')

    
    return trades



import db
symbols = ['VND','HAX','BSI','DGC','FTS','HBC','DXG','SCR', 'BSR','NVL','PDR','VGI','MWG','TPB','VCB','BID','VIB']
for symbol in symbols:
    df = db.GetStockData(symbol=symbol)
    # results = darvas_trading_strategy(df)
    print(f'Darvas: {symbol}')
    # print(f'{results[["Date","Stock","Close","profit","cash","shares"]]}')


    orders = find_trades(data=df,box_size=20)
    # for o in orders:
    #     pprint.pprint(o)



import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
import pandas as pd

def predict_price(symbol):
    data = db.GetStockData(symbol=symbol)
    x = np.array(range(len(data)))
    y = np.array(data['Close'])
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, shuffle=False)
    
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    
    poly_features = PolynomialFeatures(degree=10)
    x_poly = poly_features.fit_transform(x)
    
    reg = LinearRegression()
    reg.fit(x_poly, y)
    
    y_pred = reg.predict(x_poly)
    
    df = pd.DataFrame({'x':x.flatten(), 'y':y.flatten(), 'y_pred':y_pred.flatten()})
    
    df['MA10'] = df['y'].rolling(10).mean()
    df['MA20'] = df['y'].rolling(20).mean()
    df['MA50'] = df['y'].rolling(50).mean()
    
    plt.plot(df['x'], df['y'], label='Actual Price')
    plt.plot(df['x'], df['y_pred'], label='Predicted Price')
    plt.plot(df['x'], df['MA10'], label='MA10')
    plt.plot(df['x'], df['MA20'], label='MA20')
    plt.plot(df['x'], df['MA50'], label='MA50')
    plt.legend()
    plt.title("Hàm xấp xỉ đa và Moving Averages")
    plt.show()
    
#predict_price(symbol='HAX')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def moving_average(data, window, plot_type='line', show_error=True):
    close = data['Close']
    moving_avg = close.rolling(window=window).mean()
    
    if plot_type == 'line':
        plt.plot(close, label='Actual')
        plt.plot(moving_avg, label='Moving average')
        plt.legend()
        plt.title('Moving Average of Close Price')
    elif plot_type == 'scatter':
        plt.scatter(close.index, close, label='Actual')
        plt.scatter(moving_avg.index, moving_avg, label='Moving average')
        plt.legend()
        plt.title('Scatter Plot of Close Price and Moving Average')
    else:
        raise ValueError(f"Invalid plot_type: {plot_type}. Available options are 'line' and 'scatter'")
        
    if show_error:
        prediction = moving_avg[-len(close) + window:]
        error = close[window:] - prediction
        plt.figure()
        plt.plot(error, label='Error')
        plt.legend()
        plt.title('Error between Actual Close Price and Predicted Close Price')
    
    plt.show()
    
    return moving_avg

symbol='HAX'
data = db.GetStockData(symbol=symbol)
moving_avg = moving_average(data, window=20, plot_type='line')


import pandas as pd
import matplotlib.pyplot as plt

def stock_strategy(data):
    # Tính moving average cho ma10 và ma20
    data['ma10'] = data['Close'].rolling(window=10).mean()
    data['ma20'] = data['Close'].rolling(window=20).mean()
    
    # Khởi tạo một số biến
    buy = False
    holding_period = 0
    profit = 0
    trades = []
    
    # Duyệt qua từng phiên giao dịch
    for index, row in data.iterrows():
        if buy == False and row['ma10'] > row['ma20']:
            # Mua vào khi ma10 cắt lên ma20
            buy_price = row['Close']
            buy = True
            holding_period = 1
            trades.append((index, 'Buy', buy_price))
        elif buy == True:
            holding_period += 1
            if holding_period > 10 or row['ma10'] < row['ma20']:
                # Bán ra khi nắm giữ tối đa 10 phiên hoặc ma10 cắt xuống ma20
                sell_price = row['Close']
                profit += sell_price - buy_price
                buy = False
                holding_period = 0
                trades.append((index, 'Sell', sell_price))
    return profit, trades

# Tải dữ liệu cổ phiếu
#data = pd.read_csv('stock_data.csv')

# Sử dụng chương trình stock_strategy để tính toán lợi nhuận và tạo danh sách các lệnh giao dịch
profit, trades = stock_strategy(data)
print('Lợi nhuận:', profit)

# Vẽ đồ thị
plt.plot(data['Close'], label='Close Price')
plt.plot(data['ma10'], label='MA10')
plt.plot(data['ma20'], label='MA20')
plt.legend()

cumulative_profit = 0
for i, trade in enumerate(trades):
    date = trade[0]
    action = trade[1]
    price = trade[2]
    if action == 'Buy':
        plt.annotate(f'Buy: {price}', (date, price), textcoords='offset points', xytext=(-15,-10), ha='center')
        plt.scatter(date, price, color='green', marker='^')
        if i < len(trades) - 1:
            sell_trade = trades[i + 1]
            sell_price = sell_trade[2]
            profit = sell_price - price
            cumulative_profit += profit
            plt.annotate(f'Profit: {profit}', (date, price), textcoords='offset points', xytext=(15, 10), ha='center', color='blue')
    elif action == 'Sell':
        plt.annotate(f'Sell: {price}', (date, price), textcoords='offset points', xytext=(15,-10), ha='center')
        plt.scatter(date, price, color='red', marker='v')

plt.title(f'Phương pháp giao dịch cổ phiếu (Tổng lợi nhuận: {cumulative_profit})')
plt.xlabel('Thời gian')
plt.ylabel('Giá')
plt.show()


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_best_buy_point(data, window):
    # Tính toán giá trung bình
    data["average"] = data["Close"].rolling(window=window).mean()

    # Tìm điểm mua tốt nhất
    best_buy_point = (data["Close"] - data["average"]).idxmin()

    # Vẽ đồ thị giá trung bình và giá đóng cửa
    plt.plot(data.index, data["average"], label="Average Price")
    plt.plot(data.index, data["Close"], label="Close Price")

    # Ghi chú điểm mua tốt nhất
    plt.annotate("Best buy point", xy=(best_buy_point, data.loc[best_buy_point, "average"]),
                 xytext=(best_buy_point-30, data.loc[best_buy_point, "average"]+50),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    # Thiết lập các thuộc tính của đồ thị
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend(loc="best")
    plt.title("Stock Price and Average Price")

    # Hiển thị đồ thị
    plt.show()

# Sử dụng hàm với dữ liệu chứng khoán giả
#data = pd.read_csv("stock_data.csv")
plot_best_buy_point(data, 30)
