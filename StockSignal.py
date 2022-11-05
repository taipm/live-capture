import numpy as np

class StockSignal:
    def __init__(self,symbol, df_data, days) -> None:
        self.symbol = symbol.upper()
        self.df_data = df_data
        self.df = self.df_data[0:days]

    def avg_vol(self):
        return np.average(self.df['volume'])
    