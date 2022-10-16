# from TaiPM import *

from Caculator import *
from candleStick import CandleStick
import db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from IntradayData import *
from stockApi import *
from vnstock import *

sns.set()
pd.options.display.float_format='{:,.2f}'.format
pd.set_option('display.width',85)

class Stock:
    def __init__(self, name) -> None:
        self.name = name
        
        self.P = 0
        self.MAX_P = 0
        self.MIN_P = 0
        self.AVG_P = 0
        self.Money = 0
        
        self.V = 0
        self.MAX_V = 0
        self.MIN_V = 0
        self.AVG_V = 0

        self.df_data = pd.DataFrame()
        self.StrSummary = self.name
        self.FileName = ''
 
        self.df_data = self.Load_Daily_Data()
        self.df_daily_data = self.df_data
        self.df_weekly_data = split_array(arr = self.df_daily_data,sizeOf_item=5)

        self.last_price = self.df_data['Close'][0]
        self.last_volume = self.df_data['Volume'][0]
        
        self.daily_prices = self.df_data['Close']
        self.daily_volumes = self.df_data['Volume']
        self.daily_foreign = self.df_data['NN']
        self.daily_money = self.df_data['Money']
        self.daily_low_prices = self.df_data['Low']
        self.daily_high_prices = self.df_data['High']
        self.daily_open_prices = self.df_data['Open']
        self.daily_close_prices = self.df_data['Close']


        self.TCB_Data = self.load_basic_data()#price_board(self.name)
        self.Price = self.TCB_Data['Giá Khớp Lệnh'].values
        self.TCB_Suggest_Price = self.TCB_Data['TCBS định giá'].values
        self.RSI = self.TCB_Data['RSI'].values
        self.P_B = self.TCB_Data['P/B'].values
        self.P_E = self.TCB_Data['P/E'].values
        self.ROE = self.TCB_Data['ROE'].values

        self.df_intraday_data = self.load_intraday_data()
    
    def Load_Daily_Data(self) -> pd.DataFrame:
        return db.GetStockData(self.name)
    
    def load_intraday_data(self)->pd.DataFrame:
        return GetIntradayData(self.name)
        
    def load_basic_data(self):
        return price_board(self.name)

    def GetTCB(self):
        return price_board(self.name).transpose()

    def IsLoadData(self):
        if self.df_data.empty:
            return False
        return True

    # def GetDataSticks(self):
    #     df_sticks = GetSticks_Intraday(self.name)
    #     return df_sticks

    def Prepare(self):
        '''
        Chuẩn bị đầy đủ dữ liệu và sẵn sàng thực hiện tính toán
        ''' 
        if not self.IsLoadData():
            self.LoadData()
        
        self.PRICES = self.df_data['Close']
        self.VOLS = self.df_data['Volume']
        
        self.P = self.PRICES[0]
        self.MAX_P = np.max(self.PRICES)        
        self.MIN_P = np.min(self.PRICES)        
        self.AVG_P = np.mean(self.PRICES[0])

        self.V = self.VOLS[0]
        self.MAX_V = np.max(self.VOLS)
        self.MIN_V = np.min(self.VOLS)
        self.AVG_V = np.mean(self.VOLS)
        
        self.Money = self.V*self.P
        
        self.LEN_DATA = len(self.df_data)
        
        self.STICKS = self.ToCandleSticks()
        self.StrSummary += self.Describe()
        self.StrSummary += self.Suggestion()
        
    def Get_Price(self, d_str):
        #print(d_str)
        item = self.df_data[self.df_data['Date'] == dt.datetime.strptime(d_str, '%Y-%m-%d').date()]
        return item['Close'].values
    
    def Get_Volume(self, d_str):
        #print(d_str)
        item = self.df_data[self.df_data['Date'] == dt.datetime.strptime(d_str, '%Y-%m-%d').date()]
        return item['Volume'].values
    
    def GetDataItem(self, d_str):        
        item = self.df_data[self.df_data['Date'] == dt.datetime.strptime(d_str, '%Y-%m-%d').date()]
        return item
    
    def GetDataItemAtPrev(self,countOfPrevDays):
        item = self.df_data.iloc[countOfPrevDays]
        return item
    
    def GetPriceAtPrev(self,countOfPrevDays):
        return self.GetDataItemAtPrev(countOfPrevDays=countOfPrevDays)['Close']

    def Get_Profit(self,d_start_str,d_end_str):
        p1 = self.Get_Price(d_start_str)
        p2 = self.Get_Price(d_end_str)
        value = ((p2-p1)/p1)*100
        print(value)
        return value

    def GetProfitAtPrev(self,countOfPrevDay):
        last_p = self.GetLastPrice()
        prev_p = self.GetPriceAtPrev(countOfPrevDays=countOfPrevDay)
        return ((last_p-prev_p)/prev_p)*100

    def Get_LastTrans_Date(self):
        return self.df_data['Date'][0]
    def GetLastPrice(self):
        return self.df_data['Close'][0]

    def ToCandleSticks(self):
        sticks = list()
        for i in range(0,self.LEN_DATA):
            stick = CandleStick(high = self.df_data['High'][i],
                                close = self.df_data['Close'][i],
                                open = self.df_data['Open'][i],
                                low = self.df_data['Low'][i],
                                volume = self.df_data['Volume'][i],
                                index = i)
            sticks.append(stick)            
    
        return sticks
    
    
    def Get_TyLeSong(self,T,percent):
        """
        Tỷ lệ sóng: Là số lần dao động cao trên khung thời gian
        - T: Là khung thời gian (số phiên)
        - percent: Tỷ lệ đo sóng (thường khoảng 3% trở lên được xem là dao động mạnh)
        Kết quả:
        -1: Là lỗi (vượt quá không gian dữ liệu)
        """
        
        if(T > self.LEN_DATA):
            return -1 #Lỗi
        df = self.df_data[0:T] #Cắt dữ liệu cho khớp với số phiên
        sticks = self.STICKS[0:T] #Lấy số nến
        count_amp = 0 #Đếm biên độ dao động
        for stick in sticks:
            if np.abs(stick.Percent())>= percent:
                count_amp += 1
        
        return count_amp/T
        
    def AllForecasts(self): #Dự báo (forecast), hàm này quét toàn bộ dự báo của các nến
        up_forecasts = list()
        down_forcecasts = list()

        for i in range(0,self.LEN_DATA):
            stick = self.STICKS[i]           
            forecast_Up = False
            forecast_Down = False
            
            note = ""          
            if(stick.Forecast_By_CandleStick() == True): #Đang tạm thời có chỉ báo fly
                forecast_Up = True
                note = f'F- + {"{:.2f}".format(self.STICKS[i].Percent())}'
                up_forecasts.append([i,self.df_data['Close'][i],note])
            
            elif(stick.Forecast_By_CE() == True):
                forecast_Up = True
                note = f'CE- + {"{:.2f}".format(self.STICKS[i].Percent())}'
                up_forecasts.append([i,self.df_data['Close'][i],note])
            elif(stick.IsSell_SignalCandleStick() == True):
                forecast_Down = True
                note = f'S-InvertFly- + {"{:.2f}".format(self.STICKS[i].Percent())}'
                down_forcecasts.append([i,self.df_data['Close'][i],note])
                
        #print("Có: " + str(len(forecasts)) + " điểm dự báo")
        return up_forecasts #,down_forcecasts
    
    def CheckForecasts(self, T_n): #Nên check đến T10 (là quá mức)
        forecasts = self.AllForecasts()
        rs = list()
        
        for f in forecasts:
            index = f[0]#Chỉ số
            price = f[1]#Giá tại lúc dự báo (tăng)
            note = f[2] #Ghi chú, tăng vì lý do gì
            
            if(index < T_n): #len(self.df_data)-10
                next_index = -1
                next_price = np.max(self.df_data['Close'][index-T_n:index]) #Lấy giá lớn nhất trong khoảng này
                isCorrect = False
                if (next_price > price):
                    isCorrect = True
                    next_index = list(self.df_data['Close']).index(next_price)#[index+1:index+T_n].index(next_price)                
                rs.append([index,next_index,price,next_price,isCorrect])            
            
        #Chuyển dự báo thành ma trận dự báo
        #df_forecasts = pd.DataFrame(data=rs, columns=['T0','TN','Price','T3-P','YN'])
        #print(df_forecasts.head().to_markdown())
        return rs
    
    def Describe(self):
        
        output = f'{self.name.upper()}- Last date: {self.Get_LastTrans_Date()}'
        output += f'\nGiá cao nhất: {str(self.MAX_P)} | Giá thấp nhất: {str(self.MIN_P)} | Giá hiện tại: {self.P}'
        output += f'\n&CN: {"{:.2f}".format(((self.P - self.MAX_P)/self.MAX_P)*100)} (%) | &TN: {"{:.2f}".format(((self.P - self.MIN_P)/self.MIN_P)*100)} (%)'
        output += f'\n05 (phiên): {self.GetPriceAtPrev(5)} | {"{:.2f}".format(self.GetProfitAtPrev(5))} (%)'
        output += f'\n10 (phiên): {self.GetPriceAtPrev(10)} | {"{:.2f}".format(self.GetProfitAtPrev(10))} (%)'
        output += f'\n20 (phiên): {self.GetPriceAtPrev(20)} | {"{:.2f}".format(self.GetProfitAtPrev(20))} (%)'
        output += f'\nKL cao nhất: {str(self.MAX_V)} | KL thấp nhất: {str(self.MIN_V)}'
        output += f'\nThanh khoản cao nhất: {str(np.max(self.df_data["Money"]))} | Thanh khoản thấp nhất: {str(np.min(self.df_data["Money"]))}'
        output += f'\nNến hiện tại {self.STICKS[0].Describe()}'

        analysis_intraday = AnalysisIntradayData(symbol=self.name)
        output += f'\nAnalysis IntradayData:\n{analysis_intraday.GetSummary()}\n'

        #output += f'\nDự báo (nến) {self.STICKS[0].Forecast_By_CandleStick()}'
        output += f'\nDự báo (nến) {getMaxStickVolume(self.name).to_markdown()}'
        output += f'\nCác dự báo quá khứ: '
        rs = ""
        for x in self.AllForecasts()[0:10]:
            rs += '\n-> Phiên thứ: ' + str(x[0]) + ' | Giá : ' + str(x[1])
        output += rs
        
        #In kiểm tra dự báo
        #check_forecasts = self.CheckForecasts(T_n=30)
        # for item in check_forecasts:
        #     print(str(item))
        return output
    
    '''
    CÁC HÀM BỔ TRỢ (DỰA TRÊN CÁC KHÁI NIỆM MỚI)
    '''
    def Suggestion(self):
        #Tính toán 03 phiên
        n_days = 3
        p_amp = self.GetPriceDeeps(days=n_days,start=0) #Phiên hiện tại (start = 0)
        p_max_amp = self.MaxGain(days=n_days)
        p_min_amp = self.MaxLoss(days=n_days)

        output = ""
        output += f'\nTrong {n_days} phiên đã tăng/giảm {"{:.2f}".format(p_amp)} %.'
        output += f'\nBiến động (tăng) lớn nhất: {n_days} phiên là {"{:.2f}".format(p_max_amp)} %.'
        output += f'\nBiến động (giảm) lớn nhất: {n_days} phiên là {"{:.2f}".format(p_min_amp)} %.'
        
        if(p_amp >= 10): #Đã tăng khá rồi
            output += '\nĐã tăng cao. Xem xét bán chốt lời hoặc hạn chế mua'
        elif p_amp <=-10:
            output += '\nĐã giảm sâu. Xem xét mua thêm'
        else:
            output += '\nBiến động chưa nhiều. Theo dõi'
        return output

    def GetPriceDeeps(self, days, start): #Độ sâu biến động giá trong n phiên
        '''
        Được tính bằng giá đóng cửa hiện tại (bắt đầu bằng start) so với giá đóng cửa của n phiên lúc trước
        '''
        
        price = self.PRICES[start] #Phiên bắt đầu
        p_prev = self.PRICES[start + days-1] #Phiên kết thúc (dùng để so sánh)

        p_amp = ((price - p_prev)/p_prev)*100 # Tính theo %
        return p_amp

    # def GetProfit(symbol,start,end):
    #     #start = "01/01/2015"
    #     #end  = dt.datetime.now().strftime("%d/%m/%Y")
    #     company = symbol
    #     df_stock = investpy.get_stock_historical_data(stock= company, country= 'vietnam', from_date = start, to_date = end)
    #     p_start = df_stock['Close'][0]
    #     p_end = df_stock['Close'][-1]
    #     profit = ((p_end-p_start)/p_start)*100
    #     print(f'{p_start} -> {p_end}')
    #     return profit

    
    def MaxGain(self,days):
        lst = list()
        start = 0
        stop = self.LEN_DATA - days
        for i in range(start,stop):
            lst.append(self.GetPriceDeeps(days=days,start=i))
        #print(np.max(lst))
        return np.max(lst)

    def MaxLoss(self,days):
        lst = list()
        start = 0
        stop = self.LEN_DATA - days
        for i in range(start,stop):
            lst.append(self.GetPriceDeeps(days=days,start=i))
        #print(np.min(lst))
        return np.min(lst)
        
    #TRỰC QUAN HÓA DỮ LIỆU
    def draw(self):
        fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(10,4), sharey=True, dpi=120)

        ax1.plot(self.PRICES, 'go-')
        ax2.plot(self.PRICES, 'ro-')
        ax3.plot(self.PRICES, 'bo-')

     
        plt.tight_layout()
        plt.show()    
        
    def DrawWithForcecast(self,N):
        """
        Dự báo cho một nến

        Args:
            N (_type_): _description_
        """
        plt.rcParams["figure.figsize"] = (15,10)        
        x = range(0,N)
        
        y = self.df_data['Close'][0:N]
        y_low = self.df_data['Low'][0:N]
        y_high = self.df_data['High'][0:N]
        y_open = self.df_data['Open'][0:N]
        #y_CE = self.df_data['Open'][0:N] 
        plt.title(self.name)
        plt.plot(x,y,'b-')
        plt.plot(x,y_low,'r-')
        plt.plot(x,y_high,'y-')
        plt.plot(x,y_open,'g-')
        plt.legend()
        forecasts = self.AllForecasts()
        for i in range(0,len(forecasts)):
            index = forecasts[i][0]
            price = forecasts[i][1]
            note = forecasts[i][2]
            if(note == "CE"):
                plt.annotate(note + f'\n{index}',(index,price),arrowprops=dict(facecolor='orange', shrink=0.05))
            else:
                plt.annotate(note + f'\n{index}',(index,price),arrowprops=dict(facecolor='blue', shrink=0.05))
            # if i%2 == 0:
            #     plt.annotate("Chẵn",(x[i],y[i]))
        #plt.legend()
        plt.show()

    def DrawWithForcecasts(self,N):
        """
        Dự báo cho nhiều tín hiệu liên tiếp

        Args:
            N (_type_): _description_
        """
        plt.rcParams["figure.figsize"] = (15,10)        
        x = range(0,N)
        y = self.df_data['Close'][0:N]
        plt.title(self.name + " : TÍN HIỆU + VOL")
        plt.plot(x,y)
        forecasts = self.AllForecasts()
        for i in range(0,len(forecasts)):
            index = forecasts[i][0]
            price = forecasts[i][1]            
            note = forecasts[i][2]
            
            #Bổ sung điều kiện
            #Các phiên phía trước
            so_phien_vol = 15
            start = index
            end = index + so_phien_vol
            
            if(end <= len(self.df_data)):
                #Dự báo tại stick hiện tại                
                stick = self.STICKS[index]
                #stick_01 = self.STICKS[index+1]
                #stick_02 = self.STICKS[index+2]
                
                #check_vol = stick.VOL >= np.max([stick_01.VOL, stick_02.VOL])
                #check_vol = stick.VOL >= np.median(self.df_data[start:end].Volume)
                check_vol = stick.CLOSE <= np.mean(self.df_data[start:end].Close)
                if (check_vol):
                    if(note == "CE"):
                        plt.annotate(note + f'\n{index}',(index,price),arrowprops=dict(facecolor='orange', shrink=0.05))
                    else:
                        plt.annotate(note + f'\n{index}',(index,price),arrowprops=dict(facecolor='blue', shrink=0.05))                
        plt.legend()
        plt.show()
        

# s = Stock(name="VND")
# s.Prepare()
# s.draw()
# print(s.TCB_Suggest_Price)
# print(s.RSI)
# print(s.Price)
# print(s.df_weekly_data)
# # item = s.GetDataItemAtPrev(5).values
# # print(item)
# print(s.Describe())
# #p = s.GetPrice('2022-08-05')
#p = s.Get_Profit('2022-08-01','2022-08-05')
# print(p)
#s.DrawWithForcecast(N=30)
#print(s.StrSummary)