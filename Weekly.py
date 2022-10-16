import db

class AnalysisStock:
    pass

class AnalysisDaily:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        
        self.df_data = db.get_stock_data_from_api(symbol=self.symbol)
        self.Prices = self.df_data['Price']
        self.Volumes = self.df_data['Volume']

        self.MaxPrice = self.Prices.max()
        self.MinPrice = self.Prices.min()

        self.MaxVol = self.Volumes.max()
        self.MinVol = self.Volumes.min()
        
        self.countOf_Day = len(self.df_data)
        self.countOf_Week = self.countOf_Day/5
        self.countOf_Month = self.countOf_Week/4
        self.countOf_Year = self.countOf_Month/12

    



class AnalysisWeekly:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.df_data = db.get_stock_data_from_api(symbol=self.symbol)
        
        self.countOf_Day = len(self.df_data)
        self.countOf_Week = self.countOf_Day/5
        self.countOf_Month = self.countOf_Week/4
        self.countOf_Year = self.countOf_Month/12
    
    def SummaryData(self):
        pass

    def split_Data_To_Weekly(self):

        pass

class AnalysisMonthly:
    pass

class AnalysisYearly:
    pass