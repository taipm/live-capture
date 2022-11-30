import datetime
from RichNumber import RichNumber
from UrlCrawler import UrlCrawler as crawler
import pandas as pd
import numpy as np
from Constant import *

class StockOwners:
    def __init__(self,symbol) -> None:
        self.symbol = symbol.upper()
        self.url = f'https://s.cafef.vn/Lich-su-giao-dich-{self.symbol}-4.chn#data'
        self.df_data = self.getData()

    def getData(self):
        tables = crawler.getTables(self.url)
        if tables is None:
            return None
        else:
            table = tables[2].iloc[2:]
            df = table
            df['Owners'] = df[1].map(lambda x: x[0:15] if len(x) >= 15 else x)
            df['Position'] = df[2].map(lambda x: x[0:10] if len(str(x)) >= 10 else x)
            df['Before'] = df[5].map(lambda x: float(x)/thousand)
            df['RegBuy'] = df[6].map(lambda x:float(x)/thousand).fillna(0)
            df['RegSell'] = df[7].map(lambda x:float(x)/thousand if x is not pd.NA else 0).fillna(0)
            df['RegBuyStartDate'] = df[8].fillna('')
            df['RegBuyEndDate'] = df[9].fillna('')
            df['ResultBuy'] = df[10].map(lambda x:float(x)/thousand).fillna(0)
            df['ResultSell'] = df[11].map(lambda x:float(x)/thousand).fillna(0)
            df['ResultDate'] = df[12].fillna('')
            df['After'] =  df[13].map(lambda x:float(x)/thousand).fillna(0)
            df['%'] = df[14].map(lambda x: float(x))
            
            del_colums = [0,1,2,3,4,14,5,6,7,8,9,10,15,11,12,13,'Position','After']
            for c in del_colums:
                del df[c]
            df = df[df['RegBuyStartDate'].map(lambda x: str(datetime.datetime.today().year) in x)]
            return df

    def total_reg_buy(self)->float:
        df = self.df_data[(self.df_data['RegBuy'] > 0)]
        df = df[df['ResultBuy']==0]
        total = np.sum(df['RegBuy'])
        return total*thousand

    def total_reg_sell(self)->float:
        df = self.df_data[(self.df_data['RegSell'] > 0)]
        df = df[df['ResultSell']==0]
        total = np.sum(df['RegSell'])
        return total*thousand

    def analysis(self):
        output = f'\nCỔ ĐÔNG NỘI BỘ'
        output += f'\n{self.df_data.to_markdown()}'
        output += f'\n\nĐăng ký mua: {RichNumber(self.total_reg_buy()).toText()} | Bán: {RichNumber(self.total_reg_sell()).toText()} | Tổng: {RichNumber(self.total_reg_buy()-self.total_reg_sell()).toText()}'
        return output

    def summaryToBlog(self):
        output = f'\nCỔ ĐÔNG NỘI BỘ'
        output += f'\n{self.df_data[0:5].to_html()}'
        output += f'\n\nĐăng ký mua: {RichNumber(self.total_reg_buy()).toText()} | Bán: {RichNumber(self.total_reg_sell()).toText()} | Tổng: {RichNumber(self.total_reg_buy()-self.total_reg_sell()).toText()}'
        return output

    def __str__(self) -> str:
        return self.analysis()


