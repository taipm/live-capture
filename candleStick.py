import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
pd.options.display.float_format='{:,.2f}'.format
pd.set_option('display.width',85)

class CandleStick:
    
    def __init__(self, open, high, close, low, volume, index) -> None:
        self.OPEN = open
        self.HIGH = high
        self.CLOSE = close
        self.LOW = low
        self.VOL = volume
        self.INDEX = index
        
        self.Events = "" #Nếu có thông tin
        #Có thể bổ sung một số thông tind dể làm giàu dữ liệu
    
    def Prepare(self):    
        #Color
        COLORS = ["GREEN","RED","YELLOW","PINK","BLUE", "ORRANGE", "BLACK"]
        
        self.COLOR = None

        #GREEN - 0
        if(self.CLOSE > self.OPEN):
            self.COLOR = COLORS[0]
        #RED -1
        elif(self.CLOSE < self.OPEN):
            self.COLOR = COLORS[1]
        
        #YELLOW - 2
        elif(self.CLOSE == self.OPEN):
            self.COLOR = COLORS[2]
        
        #PINK - 3
        elif(self.CLOSE >= self.CE): #Trần -> Tím
            self.COLOR = COLORS[3]
        
        #BLUE-GREEN (TA CHUYỂN SANG BLUE) - 4
        elif(self.CLOSE <= self.FL): #Sàn -> Xám
            self.COLOR = COLORS[4]
        
        #NẾN MẠNH NHẤT NGÀY - 5
        elif(self.CLOSE == self.HIGH): #DragonFly
            self.COLOR = COLORS[5]
        
        #NẾN YẾU NHẤT NGÀY - 6
        elif(self.CLOSE == self.LOW): #DragonFly
            self.COLOR = COLORS[6]

    def IsDragonFly(self): #Nến đảo chiều tăng (là dạng nến trọc đầu, nến chân dài tới đầu luôn)
        '''
        Đây là loại nến cực kỳ đặc biệt, đánh dấu đảo chiều tăng, nếu như nó đang ở xu hướng giảm một số phiên trước mà gặp nến này thì khả năng cao là sẽ đảo chiều tăng.
        Nến này cho thấy lực mua rất mạnh, lực bán cạn kiệt, cho nên đẩy lên giá cao nhất trong ngày.
        Kết hợp: Nếu VOL thấp nữa thì càng tốt
        '''
        if (self.CLOSE == self.HIGH) and (self.CLOSE >= self.OPEN):
            return True
        return False

    def IsInvertedDragonFly(self): #Nến đảo chiều tăng (là dạng nến trọc đầu, nến chân dài tới đầu luôn)
        '''
        Đây là loại nến cực kỳ đặc biệt, đánh dấu đảo chiều tăng, nếu như nó đang ở xu hướng giảm một số phiên trước mà gặp nến này thì khả năng cao là sẽ đảo chiều tăng.
        Nến này cho thấy lực mua rất mạnh, lực bán cạn kiệt, cho nên đẩy lên giá cao nhất trong ngày.
        Kết hợp: Nếu VOL thấp nữa thì càng tốt
        '''
        if (self.CLOSE == self.LOW):
            return True
        return False
    
    def IsRed(self):
        if self.OPEN < self.CLOSE:
            return True
        return False
    
    def IsGreen(self):
        if self.OPEN > self.CLOSE:
            return True
        return False
    
    def IsYellow(self):
        if self.OPEN == self.CLOSE:
            return True
        return False
    
    def IsMarubozu(self): #Nến sọ dừa, không đầu không chân
        '''
        https://dautuhanghoa.vn/bai-2-nen-nhat-nhung-mau-nen-co-ban/
        https://www.investo.vn/chung-khoan/chi-so/mo-hinh-nen-nhat-va-cach-doc-cac-loai-nen-co-ban/
        https://pinetree.vn/post/20210622/bieu-do-nen-nhat-candlestick-charting-cach-doc-phan-tich-mo-hinh-nen-va-y-nghia-cac-loai-nen-trong-phan-tich-ky-thuat-chung-khoan/
        '''
        pass

    def IsHammer(self): #Nến Hammer, là dạng nến xanh, nếu nến đỏ gọn là HangingMan
        '''
        https://www.investo.vn/chung-khoan/chi-so/mo-hinh-nen-nhat-va-cach-doc-cac-loai-nen-co-ban/
        https://vn.mitrade.com/others/phan-tich-ky-thuat/mo-hinh-nen-nhat-bieu-do-nen-nhat
        '''
        pass

    def IsHangingMan(self): #Nến treo cổ
        '''
        https://www.investo.vn/chung-khoan/chi-so/mo-hinh-nen-nhat-va-cach-doc-cac-loai-nen-co-ban/
        '''
        pass
    
    def Percent(self):
        try:
            return (((self.CLOSE - self.OPEN))/self.OPEN)*100
        except:
            print(f'Lỗi: {self.INDEX} at {self.OPEN} Or {self.CLOSE}')
            return None
    
    def Head(self): #Đầu nến
        x = -1 #Âm là lỗi
        if self.IsRed():
            x = self.HIGH - self.OPEN
        else: #Xanh hoặc vàng
            x = self.HIGH - self.CLOSE
                    
        return x
    
    def Tail(self): #Chân
        y = -1 #Âm là lỗi
        if self.IsRed():
            y = self.CLOSE - self.LOW
        else: #Xanh hoặc vàng
            y = self.OPEN - self.LOW
                    
        return y
    
    def Body(self): #Thân
        return np.abs(self.OPEN-self.CLOSE)

    def Len(self): #Độ dài nến
        return self.HIGH - self.LOW
    
    def Get_MarkWave(self): #Điểm sức mạnh gợn sóng tính theo thời gian (là số phiên (i) cách phiên hiện tại)
        #Là tỷ lệ nghịch với khoảng cách
        if(self.INDEX == 0):
            return 1
        return 1/self.INDEX
  
    def CE(self):
        return self.OPEN + self.OPEN*6.8/100 #Gần đúng thôi, bữa nào rảnh rỗi cài đặt lại, có làm tròn giá cho khớp
    
    def Is_CE(self):
        if self.Percent() >= 6:
            return True
        return False
    
    def FL(self):
        return self.OPEN - self.OPEN*6.8/100

    def Percent(self): #Độ sâu
        if self.OPEN != 0:
            return ((self.CLOSE - self.OPEN)/(self.OPEN))*100
        return -100
    
    def Forecast_By_CandleStick(self): #Dự báo dựa trên một số tiêu chí
        result = None        
        if self.IsDragonFly():
            result = True            
        return result
    
    def IsSell_SignalCandleStick(self):
        """
        Lấy các tín hiệu BÁN
        (1) - Khi gặp nến bẹp đầu (InvertedHammer) thì bán
        (2) - Khi tạo đỉnh thì bán
        """
        result = None        
        if self.IsInvertedDragonFly(): #Bán mạnh nhất
            result = True
        return result


    def Forecast_By_CE(self): #Khi CE thì nó sẽ tăng tiếp
        result = None    
        if self.Is_CE():
            result = True            
        return result
    
    def Describe(self): #Thông tin nến
        output = ""
        output+= f'\nĐiểm : {self.Get_MarkWave()}'
        
        return output
    
    def IsBuy_UpSignal(self):
        '''
        Nếu có tín hiệu tăng trả về True, còn ngược lại thì chưa biết.
        Tín hiệu được dự đoán là tăng khi [NẾN TRONG NGÀY]:
        (1) - Là DragonFly (Tuy nhiên cần kiểm tra thêm nó ở dưới đáy hay trên đỉnh dựa vào các nến phía trước nữa, đây chỉ là điều kiện cần chứ chưa đủ)
        Hoặc (2) - Nó đóng cửa ở giá cao nhất (Trần) - Trường hợp này cũng là một trường hợp của DragonFly (tuy nhiên vì Trần là một tín hiệu dễ thấy nên ta để luôn)
        '''
        if self.Is_CE():
            return True
        
        if (self.IsDragonFly()):
            return True

        return False

    def IsBuy_DownSignal(self):
        pass

    def Is_Skip(self):
        pass

    def Print(self):
        print(self.Describe())

    def Get_Summary(self):
        return self.Describe()
    
    def Draw(self): #Vẽ nến
        pass


def Test():
    H = 10
    L = 5
    O = 4
    C = 4.5
    V = 1000
    
    for i in [0,1,2,3,4,5]:
        s = CandleStick(open=O,high=H,close=C,low=L,volume=V, index=i)
        s.Print()
#Test()