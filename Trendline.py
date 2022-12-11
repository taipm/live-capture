import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
from db import *

symbol = 'VND'
data = GetStockDataForTrendline(symbol=symbol)[0:5*26]
df = data.copy()
data = df

data0 = data.copy()
data0['date_id'] = ((data0.index.date - data0.index.date.min())).astype('timedelta64[D]')
data0['date_id'] = data0['date_id'].dt.days + 1

# high trend line

data1 = data0.copy()

while len(data1)>3:

    reg = linregress(
                    x=data1['date_id'],
                    y=data1['High'],
                    )
    data1 = data1.loc[data1['High'] > reg[0] * data1['date_id'] + reg[1]]

reg = linregress(
                    x=data1['date_id'],
                    y=data1['High'],
                    )

data0['high_trend'] = reg[0] * data0['date_id'] + reg[1]
print(f'Cản hiện tại: {data0.iloc[0]["high_trend"]}')

# low trend line

data1 = data0.copy()

while len(data1)>3:

    reg = linregress(
                    x=data1['date_id'],
                    y=data1['Low'],
                    )
    data1 = data1.loc[data1['Low'] < reg[0] * data1['date_id'] + reg[1]]

reg = linregress(
                    x=data1['date_id'],
                    y=data1['Low'],
                    )

data0['low_trend'] = reg[0] * data0['date_id'] + reg[1]


#THỜI GIAN NGẮN HƠN

#data = qdl.get("WIKI/AAPL", start_date="2007-01-01", end_date="2017-05-01")
data = GetStockDataForTrendline(symbol=symbol)[0:5*4*3]
df = data.copy()
data = df

data2 = data.copy()
data2['date_id'] = ((data2.index.date - data2.index.date.min())).astype('timedelta64[D]')
data2['date_id'] = data2['date_id'].dt.days + 1

# high trend line

data2 = data2.copy()

while len(data2)>3:

    reg = linregress(
                    x=data2['date_id'],
                    y=data2['High'],
                    )
    data2 = data2.loc[data2['High'] > reg[0] * data2['date_id'] + reg[1]]

reg = linregress(
                    x=data2['date_id'],
                    y=data2['High'],
                    )

data2['high_trend'] = reg[0] * data2['date_id'] + reg[1]
print(f'Cản hiện tại: {data2.iloc[0]["high_trend"]}')

# plot

data0['Close'].plot()
data0['high_trend'].plot()
data0['low_trend'].plot()
data2['high_trend'].plot()
plt.show()



# import matplotlib.pyplot as plt
# import numpy as np
    
# up = []
# dn = []
# up.append(1.00)
# dn.append(1.25)
    
# for i in range(1, 25):
#     dn.append(dn[i-1] / 1.0015)
#     up.append(up[i-1] * 1.003)

# #We absolutely do not know what the trend lines should be in the future.
# koef_up = up[len(up)-1] / up[len(up)-2]#get coeficents up
# koef_dn = dn[len(up)-2] / dn[len(up)-1]#get coeficents dn
# print('koef_up', koef_up, 'koef_dn', koef_dn)

# for i in range(25, 30):
#     up.append(up[i-1] * koef_up)#calculate line to the future up
#     dn.append(dn[i-1] / koef_dn)#calculate line to the future dn

# ind = np.arange(30)
# fig, ax = plt.subplots()
# ax.plot(ind, up, color="green")
# ax.plot(ind, dn, color="red")
# ax.plot(ind[25:], up[25:], color="yellow")
# ax.plot(ind[25:], dn[25:], color="yellow")
# fig.autofmt_xdate()
# plt.show()