import datetime
from MongoDb import MongoDb
from Recommend import Recommend

class RecommendDb(MongoDb):
    def __init__(self, recommendLst:list, type_recommend:str, date_recommend:datetime) -> None:
        super().__init__(name="Recommends")
        self.recommends = recommendLst
        self.type_recommend = type_recommend
        self.date_recommend = date_recommend


    def saveAll(self):
        for symbol in self.recommends:
            self.addItem(Recommend(symbol=symbol,type_recommend=self.type_recommend, date_recommend=self.date_recommend))

# lst = ["BSR", "GAS", "DPM", "REE"]
# #r = RecommendDb(recommendLst=lst,type_recommend='MA-GIAO NHAU', date_recommend='2022-12-02 21:10:46.529476')
# r = RecommendDb(recommendLst=lst,type_recommend='MA-GIAO NHAU', date_recommend=str(datetime.datetime.now()))

# # r.deleteAll()
# print('Lưu')
# r.saveAll()

# lst = r.getAll()
# print(lst)

# print('Xóa')
# r.deleteItemsOfToday()

# lst = r.getAll()
# print(lst)


    