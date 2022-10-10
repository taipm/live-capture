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
        market_price = db.get_stock_data_from_api(symbol=symbol).iloc[0]['Close']*1000
        m_price = market_price

        new_vol = Caculator.EvaluationOrder(old_vol=vol,old_price=price,ratio_profit=ratio, market_price=m_price)
        sum_vol = vol + new_vol
        sum_money = vol*price + new_vol*m_price
        avg_price = sum_money/sum_vol
        buy_money = new_vol*m_price
        output_text = f'{symbol} - Mua {new_vol:,.0f} ~ Tiền (mua): {buy_money:,.0f}\n' +\
                f'{symbol} - T_Vol: {sum_vol:,.0f} - Giá: {avg_price:,.2f} ({percent(m_price,avg_price):.2f} (%)) | {sum_money:,.0f}'
                ##f'Giá TB (mới): {avg_price:,.2f} - Profit: {percent(m_price,avg_price):.2f} (%)' +\
        return output_text

    elif(len_items == 4):
        symbol = items[0]
        vol = float(items[1])
        price = float(items[2])
        target_price = float(items[3])
        money = vol*price
        
        print(f'{symbol} {vol} {price} m_price: {target_price}')
        ratio = -3/100        
        #market_price = db.get_stock_data_from_api(symbol=symbol).iloc[0]['Close']*1000
        #m_price = market_price

        new_vol = Caculator.EvaluationOrder(old_vol=vol,old_price=price,ratio_profit=ratio, market_price=target_price)
        sum_vol = vol + new_vol
        sum_money = vol*price + new_vol*target_price
        avg_price = sum_money/sum_vol
        buy_money = new_vol*target_price
        output_text = f'{symbol}\n' +\
                f'Hiện tại: Vol {vol:,.0f} - Giá TB: {price:,.2f} = Tiền: {money:,.0f}\n' +\
                f'Mua {new_vol:,.0f} Giá: {target_price:,.2f} = Tiền (mua): {buy_money:,.0f}\n' +\
                f'Kết quả:\n {symbol} - Vol: {sum_vol:,.0f} - Giá TB: {avg_price:,.2f} ({percent(target_price,avg_price):.2f} (%)) = Tiền: {sum_money:,.0f}'
                ##f'Giá TB (mới): {avg_price:,.2f} - Profit: {percent(m_price,avg_price):.2f} (%)' +\
        return output_text

    else:
        return ""


#def planning()

print(parseTextCommand("VND 500 17250"))
print(parseTextCommand("VND 500 17250 13400"))