import db
symbol = 'FRT'
print(symbol)
data = db.GetStockData(symbol=symbol)
#data = data.reset_index()
print(data)
#df = data#.sort_values(by=['Date'], ascending=False).tail(100)

df = data
def find_bad_buy_points(df, profit_margin=-0.05):
    bad_buy_points = []
    for i in range(len(df) - 3):
        if ((df.iloc[i + 3]['Close'] - df.iloc[i]['Close']) / df.iloc[i]['Close']) < profit_margin:
            bad_buy_points.append((df.iloc[i]['Date'], df.iloc[i]['Close']))
    return bad_buy_points

def find_good_buy_points(df, profit_margin=0.1):
    good_buy_points = []
    for i in range(len(df) - 3):
        if ((df.iloc[i + 3]['Close'] - df.iloc[i]['Close']) / df.iloc[i]['Close']) > profit_margin:
            good_buy_points.append((df.iloc[i]['Date'], df.iloc[i]['Close']))
    return good_buy_points

good_buy_points = find_good_buy_points(df)
bad_buy_points = find_bad_buy_points(df)



# Tạo dataframe từ tập dữ liệu
#data = df#pd.read_csv('stock_data.csv')

# Xem cấu trúc của dataframe
#print(data.head())

# Tìm điểm mua tốt và điểm mua xấu
T = 3
# Định nghĩa hàm tính lợi nhuận
def calculate_return(data, index, T=3):
    return (data.loc[index + T, 'Close'] - data.loc[index, 'Close']) / data.loc[index, 'Close']

# Tìm điểm mua tốt và điểm mua xấu
buy_points = []
sell_points = []

for i in range(len(data) - T):
    return_value = calculate_return(data, i)
    if return_value >= 0.05:
        buy_points.append((data.loc[i, 'Date'], data.loc[i, 'Close'], return_value))
    elif return_value <= -0.05:
        sell_points.append((data.loc[i, 'Date'], data.loc[i, 'Close'], return_value))

# In ra điểm mua tốt và điểm mua xấu
print('Buy points:')
for bp in buy_points:
    print(bp)
    
print('Sell points:')
for sp in sell_points:
    print(sp)

# Đánh giá mức giá hiện tại là tốt hay xấu
# current_price = data.loc[len(data) - 1, 'Close']
# current_date = data.loc[len(data) - 1, 'Date']
# return_value = calculate_return(data, len(data) - T - 1)

def forecast(index):
    _data = data[0:len(data) - index + 1]
    current_price = _data.loc[index, 'Close']
    current_date = _data.loc[index, 'Date']
    return_value = calculate_return(data, len(data) - T - 1)


    if return_value >= 0.05:
        print(f'The current price is {current_price} | {current_date} of {symbol} is a buy point, return: {return_value}')
    elif return_value <= -0.05:
        #print(f'The current price is a sell point, return: {return_value}')
        print(f'The current price is {current_price} | {current_date}  of {symbol} is a sell point, return: {return_value}')
    else:
        print(f'The current price is {current_price} | {current_date}  of {symbol} is neutral, return: {return_value}')
    
    if return_value >= 0.05:
        print(f'The current price is {current_price} of {symbol} is a buy point, return: {return_value}')
        plt.scatter(current_date, current_price, color='green', label='Dự báo tốt')
    elif return_value <= -0.05:
        #print(f'The current price is a sell point, return: {return_value}')
        plt.scatter(current_date, current_price, color='yellow', label='Dự báo xấu')
        #print(f'The current price is {current_price} of {symbol} is a sell point, return: {return_value}')
    else:
        print(f'The current price is {current_price} of {symbol} is neutral, return: {return_value}')
    
    return return_value
    #print(f'The current price is neutral, return: {return_value}')


import matplotlib.pyplot as plt

plt.plot(df['Date'], df['Close'], label='Close Price')
for date, close in good_buy_points:
    plt.scatter(date, close, color='blue', label='Good Buy Point' if len(good_buy_points) == 1 else None)
for date, close in bad_buy_points:
    plt.scatter(date, close, color='red', label='Bad Buy Point' if len(bad_buy_points) == 1 else None)


for index in range(5):
    forecast(index=index)

plt.legend()
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Good and Bad Buy Points')
plt.show()