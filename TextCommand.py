import Caculator
from vnstock import *
import db
from helpers import percent
from stock import Stock

def parseTextCommand(text):
    items = text.split(' ')
    len_items = len(items)

    if(len_items == 3):
        #LỆNH TÍNH TOÁN
        symbol = items[0]
        vol = float(items[1])
        price = float(items[2])
        
        print(f'{symbol} {vol} {price}')

        ratio = -3/100
        # stock = Stock(name=symbol)
        # stock.Prepare()
        # m_price = stock.P*1000
        # print(m_price)
        market_price = db.get_stock_data_from_api(symbol=symbol).iloc[0]['Close']*1000
        #print(market_price)
        m_price = market_price

        new_vol = Caculator.EvaluationOrder(old_vol=vol,old_price=price,ratio_profit=ratio, market_price=m_price)
        sum_vol = vol + new_vol
        sum_money = vol*price + new_vol*m_price
        avg_price = sum_money/sum_vol
        buy_money = new_vol*m_price
        output_text = f'{symbol} - Mua {new_vol:,.0f} ~ Tiền: {buy_money:,.0f}\n' +\
                f'{symbol} - T_Vol: {sum_vol:,.0f} - {avg_price:,.2f} ({percent(m_price,avg_price):.2f} (%)) | {sum_money:,.0f}'
                ##f'Giá TB (mới): {avg_price:,.2f} - Profit: {percent(m_price,avg_price):.2f} (%)' +\
        return output_text
    else:
        return ""


#def planning()

print(parseTextCommand("VND 500 17250"))