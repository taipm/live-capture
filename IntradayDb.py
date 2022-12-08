from MongoDb import MongoDb
from db import *
from DateHelper import *

class IntradayDb(MongoDb):
    def __init__(self, name, symbol) -> None:
        super().__init__(name=name)

        self.symbol = symbol.upper()
        self.db_file_path = './data/' + self.symbol + '-Intraday-' + StrTODAY + ".xlsx"

    def GetLastData(self):
        df = pd.read_excel(self.db_file_path)
        return df

    def UpdateDb(self):
        df = GetIntradayData(self.symbol)
        if(not df.empty):
            df.to_excel(self.db_file_path)

