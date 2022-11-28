from DateHelper import StrTODAY
from MongoDb import ObjectDb

class DailyMarketScore(ObjectDb):
    def __init__(self) -> None:
        super().__init__()

        self.summary:str

        #DANH SÁCH CÁC CỔ PHIẾU PHÙ HỢP VỚI TIÊU CHÍ (NHƯ TÊN)
        self.CEs = []
        self.FLs = []
        self.Elephants = []
        self.GREENs = []
        self.YELLOWs = []
        self.REDs = []
        self.MaxVols = []
        self.MaxPrice = []
        self.MinVols = []
        self.MinPrice = []
        self.MA50s = [] #>=MA50
        self.MA20s = []
        self.MA10s = []
        self.MA100s = []
        self.MA200s = []

        self.VolumeUps = [] #Volume tăng liên tục
        self.VolumeDowns = [] #Volume giảm liên tục

        self.RecommendList = [] #Danh sách khuyến nghị

        #GAPS
        self.GapUps = []
        self.GapDowns = []
        
        #MÔ HÌNH THEO MẪU LÝ THUYẾT
        self.DarvasList = []
        self.SepaList = []
        self.CanslimList = []

        #THỊ TRƯỜNG CHUNG
        self.MarketIndex:float #Là điểm số thị trường
        self.MarketLiquidity:float
        self.MarketColor:str

    
    def add(self, symbol:str,type:str):
        pass

    def addCE(self, symbol:str):
        self.CEs.append(symbol)

    def addFL(self, symbol:str):
        self.FLs.append(symbol)
    
    def addGREEN(self, symbol:str):
        self.GREENs.append(symbol)
    
    def addYELLOW(self, symbol:str):
        self.YELLOWs.append(symbol)
    
    def addRED(self, symbol:str):
        self.REDs.append(symbol)

    def addElephant(self, symbol:str):
        self.Elephants.append(symbol)
    
    def process(self):
        self.CEs = set(self.CEs)

    def postToBlog(self):
        pass

    def saveToDb(self):
        pass

    def __str__(self) -> str:
        output = f'DAILY MARKET SUMMARY: {StrTODAY}'
        output += f'\nCE ({len(self.CEs)}):\n{self.CEs}'
        output += f'\nFL ({len(self.FLs)}):\n{self.FLs}'
        return output