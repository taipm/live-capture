import Caculator
from vnstock import *
import db
from DateHelper import *
from Stock import Stock

# class StockCommand:
#     # def __init__(self, symbol, request) -> None:
#     #     self.symbol = symbol
#     #     self.request = request
    
#     def __init__(self, command) -> None:
#         self.command = cl
    
#     def clean(self, command):
#         command = command


# def match_request(text):
#     stock = text.split(' ')[0]
#     request = text.split(' ')[1]
#     return StockCommand(symbl = stock, request = request)

class BotCommand:
    def __init__(self, text) -> None:
        self.text = text.strip()
    
    def is_two_numbers(self):
        if(self.text.startswith('?')):
            self.text = self.text[1:].strip()
        print(self.text)
        items = self.text.split(' ')
        print(items)
        check = True
        for item in items:
            if item.isnumeric() == False:
                check = False
                break
        if(check):
            #numbers = items
            if(len(items) == 2):
                return float(items[0]), float(items[1])
        else:
            return None

# command = BotCommand('? 1 2')
# a, b = command.is_two_numbers()
# print(percent(a,b))

def parse_request(text):
    if(text.startswith('#')):
        return "Command"
    else:
        return "Text"

# print(parse_request('#HPG'))
# print(parse_request("HPG"))

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

# print(parseTextCommand("VND 500 17250"))
# print(parseTextCommand("VND 500 17250 13400"))