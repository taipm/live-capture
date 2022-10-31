from DateHelper import *
from DayStick import *

class DayData:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.df_data = db.GetStockData(self.symbol)
        self.end_date = pd.to_datetime(self.df_data['Date'][0]).date()
        self.start_date = pd.to_datetime(self.df_data['Date'][len(self.df_data)-1]).date()
        self.count_of_days = len(self.df_data)
        self.sticks = []

    def to_string(self):
        print(f'Count of days: {self.count_of_days} - Start: {self.start_date} - End: {self.end_date}')

    def get_date_data_stick(self,date):
        data = self.df_data[self.df_data['Date'] == parse_text_to_date(str(date))]
        date_stick = DateStick(symbol=self.symbol,
            date = date,
            open = data['Open'].values,
            close = data['Close'].values,
            high = data['High'].values,
            low = data['Low'].values,
            volume= data['Volume'].values
        )
        return date_stick
    
    def get_next_stick(self, date):
        next_date = get_after_date(date)
        return self.get_date_data_stick(date = str(next_date))
    
    def get_prev_stick(self, date):
        prev_date = get_prev_date(date)
        return self.get_date_data_stick(date = str(prev_date))
    
    def to_sticks(self):
        start = self.start_date
        end = self.end_date
        delta = timedelta(days=1)
        
        while (start <= end):
            date = start
            stick = self.get_date_data_stick(date=date)
            self.sticks.append(stick)
            start += delta

        return self.sticks

    def get_forcast(self, date):
        stick = self.get_date_data_stick(date=date)
        if(stick.close == stick.low):
            return "UP"
        elif(stick.close == stick.high):
            return "UP"
        else:
            return None

    def get_check_forcast(self, date):
        current_stick = self.get_date_data_stick(date=date)
        next_date = get_next_date(str_date=date,days=3)
        next_stick = self.get_date_data_stick(date=next_date)
        print(f'{self.symbol} - Current: {current_stick.close} ({date}) - Next: {next_stick.close} ({next_date})')

        #result_of_forcast = self.get_check_forcast(date=date)

        if(current_stick.close <= next_stick.close):
            return True
        else:
            return False
    # def check_forcast(self, date):
    #     stick = self.get_date_data_stick(date=date)
    #     for days in range(0,5):
    #         next_stick

# d = DayData(symbol='FRT')
# d.to_string()
# date = "2022-10-10"
# print(d.get_forcast(date=date))
# print(d.get_check_forcast(date=date))

# sticks = d.to_sticks()
# for stick in sticks:
#     f = stick.forcast()
#     if(f):
#         print(stick.forcast())
#         print(stick.to_string())

