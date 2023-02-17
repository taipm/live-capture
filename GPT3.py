#TÌM ĐIỂM TƯƠNG ĐỒNG

import pandas as pd
import db
import pandas as pd
import numpy as np


def RSI(df, period):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = abs(delta.where(delta < 0, 0))
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def trade_strategy(df, rsi_mark):
    buy_points = df[df['RSI'] <= rsi_mark].index
    results = []
    for buy_point in buy_points:
        max_profit = df['Close'][buy_point:buy_point+10].max() / df.loc[buy_point, 'Close'] - 1
        results.append(max_profit)
    results = np.array(results)
    success = np.sum(results >= 0.07)
    total = len(results)
    success_ratio = -1
    if total > 0:
        success_ratio = success / total
    return success_ratio

#df = pd.read_csv('stock_data.csv')
def find_elephant_trades(df, ratio_up_vol):
    avg_volume = df["Volume"].rolling(window=10).mean()
    elephant_trades = []
    for i in range(10, df.shape[0]):
        if df.iloc[i]["Volume"] >= ratio_up_vol * avg_volume.iloc[i] and \
           df.iloc[i]["Close"] >= 1.02 * df.iloc[i]["Open"]:
            elephant_trades.append(i)
    print(elephant_trades)
    return elephant_trades

def calculate_elephant_success_rate(df, elephant_trades):
    success = 0
    failed = 0
    for trade in elephant_trades:
        max_return = df.iloc[trade:trade+10]["Close"].max() / df.iloc[trade]["Close"] - 1
        if max_return >= 0.07:
            success += 1
        else:
            failed += 1
    total = (success + failed)
    success_ratio = -1
    if total > 0:
        success_ratio = success / total
    return success_ratio
    #return success / 

def success_rate_at_ma_cross(data):
    data['ma10'] = data['Close'].rolling(10).mean()
    data['ma20'] = data['Close'].rolling(50).mean()
    #buys = (data['ma10'] > data['ma20']) & (data['ma10'].shift(1) <= data['ma20'].shift(1))
    buys = (data['ma10'] < data['Close'])# & (data['ma10'].shift(1) <= data['ma20'].shift(1))
    data.loc[buys, 'buy_price'] = data.loc[buys, 'Close']
    data['return'] = (data['Close'] - data['buy_price']) / data['buy_price']
    win_trades = data[data['return'] > 0].count()[0]
    lose_trades = data[data['return'] < 0].count()[0]
    total_trades = win_trades + lose_trades
    success_rate = win_trades / total_trades if total_trades > 0 else 0
    return success_rate

import matplotlib.pyplot as plt

def plot_with_trades(df, success_ratio):
    plt.plot(df['Close'], label='Close Price')
    buy_points = df[df['RSI'] <= 30].index
    success = []
    failure = []
    profits = []
    for buy_point in buy_points:
        max_profit = df['Close'][buy_point:buy_point+10].max() / df.loc[buy_point, 'Close'] - 1
        profits.append(max_profit)
        if max_profit >= 0.07:
            success.append(buy_point)
        else:
            failure.append(buy_point)
    plt.scatter(success, df.loc[success, 'Close'], c='green', label='Successful Trade')
    plt.scatter(failure, df.loc[failure, 'Close'], c='red', label='Failed Trade')
    for i, txt in enumerate(profits):
        if txt >= 0:
            plt.annotate(f"{txt:.2%}", (buy_points[i], df.loc[buy_points[i], 'Close']), color='green')
        else:
            plt.annotate(f"{txt:.2%}", (buy_points[i], df.loc[buy_points[i], 'Close']), color='red')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'Stock Price with Trades\nSuccess Ratio: {success_ratio:.2%}')
    plt.show()

def forecast(df):
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error

    # Load data
    #df = pd.read_csv("data.csv")

    # Split data into training and testing sets
    training_data = df.iloc[:-10]
    testing_data = df.iloc[-10:]

    # Train the model
    reg = LinearRegression().fit(training_data[["Volume"]], training_data["Close"])

    # Make predictions on the testing data
    predictions = reg.predict(testing_data[["Close"]])

    # Calculate the mean squared error of the predictions
    mse = mean_squared_error(testing_data["Close"], predictions)

    # Evaluate the success rate of the predictions
    success_rate = 1 - mse/testing_data["Close"].var()

    print("Success rate:", success_rate)
    return success_rate



symbols = ['HAX', 'VND', 'HBC', 'BSI']
for symbol in symbols:
    print(symbol)
    df = db.GetStockData(symbol=symbol)

    df['RSI'] = RSI(df, 14)

    rsi_marks = [20, 30, 70, 80, 90]
    for rsi_mark in rsi_marks:
        success_ratio = trade_strategy(df,rsi_mark=rsi_mark)
        print(f'Success Ratio {symbol} - RSI <= {rsi_mark}: {success_ratio*100:,.2f} (%)')
        #plot_with_trades(df, success_ratio)
    ratio_up_vol = 2
    r = calculate_elephant_success_rate(df=df,elephant_trades=find_elephant_trades(df=df,ratio_up_vol=ratio_up_vol))
    print(f'Success Ratio {symbol} - Elephants {ratio_up_vol}: {r*100:,.2f} (%)')

    success_rate = success_rate_at_ma_cross(df)
    print(f'Success Ratio MA10, MA20: {success_rate}')

    print(f'Forecast: {forecast(df=df)}')