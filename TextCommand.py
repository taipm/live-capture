from pprint import pprint
from Caculator import*
from vnstock import *
from BuyOrder import BuyOrder
from SellOrder import Order, SellOrder
from TextHelper import *
import db
from DateHelper import *
from Alpha import Alpha

class Command:
    def __init__(self, text) -> None:
        self.command = text.strip()

class MathCommand(Command):
    def __init__(self, command) -> None:        
        super().__init__(command)
        self.result = self.excute()

    def excute(self):
        return Alpha(self.command).result

    def to_string(self):
        return self.command
class StockCommand:
    """
    LỆNH: BUY(VND,100,11.2)
    Nghĩa là: Mua 100 con VND, giá 11.2
    """
    def __init__(self, command) -> None:
        self.command = command.lower().strip()    
        order = self.parse()
        self.type = order.type
        self.symbol = order.symbol.upper()
        self.volume = float(order.volume)
        self.price = float(order.price)
        self.order = order

    def tokens(self):
        try:
            type = self.command.split('(')[0]
            symbol = self.command.split('(')[1].split(',')[0]
            volume = self.command.split('(')[1].split(',')[1]
            price = self.command.split('(')[1].split(',')[2][0:len(self.command.split('(')[1].split(',')[2])-1]
            return type, symbol,volume,price
        except:
            return None
    
    def parse(self):
        '''
        VND(130000,17.2)
        VND(-1000,18.2)
        '''
        print(self.command)
        tokens = self.command.split('(')
        symbol = tokens[0].upper()
        volume = float(tokens[1].split(',')[0])
        price = float(tokens[1].split(',')[1][0:len(tokens[1].split(',')[1])-1])
        order = Order(symbol=symbol)

        if(volume >= 0):            
            order = BuyOrder(symbol=symbol,volume=volume,price=price)
        else:            
            order = SellOrder(symbol=symbol,volume=volume,price=price)
        pprint(order)
        return order

    
    def to_string(self):
        return f'{self.symbol} | {self.volume:,.0f} | {self.price:,.2f}'

class BotCommand:
    def __init__(self, text) -> None:
        self.text = text.strip()
        self.text = toStandard(self.text)
        self.tokens = self.tokens()
        
    def is_one_number(self):
        if(len(self.tokens) == 1 and self.text.isnumeric()):
            return True
        else:
            return False
            
    def tokens(self):
        return self.text.split(' ')
    
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
# b = BotCommand('a + b*c - d/e')
# print(b.tokens)

def parse_request(text):
    if(text.startswith('#')):
        return "Command"
    else:
        return "Text"

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


def is_sell_stock_command(text):
    '''
    VND(-2000,10.55) - Bán 2k VND giá 10.55
    '''
    result = True
    if('(' in text and ')' in text and ',' in text):
        items = text.split('(')
        symbol = items[0]
        if(len(symbol) == 3):
            try:
                volume = float(items[1].split(',')[0])
                if(volume < 0):
                    price = float(items[1].split(',')[1].split(')')[0])
                    print(f'{symbol} - {volume} - {price}')
                else:
                    result = False
            except:
                print('Không phải lệnh bán')
                result = False
        else:
            result = False
    else:
        result = False
    return result

def is_buy_stock_command(text):
    '''
    VND(2000,10.55) - Mua 2k VND giá 10.55
    '''
    result = True
    if('(' in text and ')' in text and ',' in text):
        items = text.split('(')
        symbol = items[0]
        if(len(symbol) == 3):
            try:
                volume = float(items[1].split(',')[0])
                if(volume > 0):
                    price = float(items[1].split(',')[1].split(')')[0])
                    print(f'{symbol} - {volume} - {price}')
                else:
                    result = False
            except:
                print('Không phải lệnh bán')
                result = False
        else:
            result = False
    else:
        result = False
    return result
# print(is_sell_stock_command('VND(-2000,10.55)'))
# print(is_sell_stock_command('VNDX(-2000,10.55)'))
# print(is_buy_stock_command('VND(-2000,10.55)'))
# print(is_buy_stock_command('VND(2000,10.55)'))
        
    