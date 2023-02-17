# from Stock import Stock


# stock = Stock(name='HAH')
# prices = stock.prices.tolist()

# # import pandas as pd
# # import matplotlib.pyplot as plt

# # df = stock.df_data.sort_values(by='Date')

# # # Tính trung bình diện và độ lệch chuẩn cho dãy giá chứng khoán
# # df['20d_mean'] = df['Close'].rolling(window=20).mean()
# # df['std'] = df['Close'].rolling(window=20).std()

# # # Tính giá trị Bollinger Bands
# # df['upper_band'] = df['20d_mean'] + 2*df['std']
# # df['lower_band'] = df['20d_mean'] - 2*df['std']

# # # Vẽ đồ thị
# # plt.figure(figsize=(12,6))
# # plt.plot(df['Close'], label='Close Price')
# # plt.plot(df['20d_mean'], label='20-day Moving Average')
# # plt.plot(df['upper_band'], label='Upper Band')
# # plt.plot(df['lower_band'], label='Lower Band')
# # plt.legend(loc='best')
# # plt.title('Bollinger Bands')
# # plt.xlabel('Date')
# # plt.ylabel('Price')
# # plt.show()



# import numpy as np
# import matplotlib.pyplot as plt

# # Input data
# df = stock.df_data.sort_values(by=['Date'],ascending=True)
# x = df['Date'].index
# y = df['Close']

# # Fit a polynomial regression model
# model = np.polyfit(x, y, 10)

# # Get the predictions
# predictions = np.polyval(model, x)

# # Plot the original data and the predictions
# plt.scatter(x, y)
# plt.plot(x, predictions, 'r')
# plt.show()
# # Get the coefficients of the polynomial
# coefficients = np.polyfit(x, y, 3)

# # Convert the coefficients to a polynomial equation
# polynomial = np.poly1d(coefficients)

# # Print the polynomial equation
# print(polynomial)

# # Predict the value for x = 6
# next_value = np.polyval(polynomial, -1)

# print(next_value)
