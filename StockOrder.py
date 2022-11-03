from DateHelper import percent

class Order:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()

class BuyOrder:
    BSC_BUY_FEE = 0.1/100

    def __init__(self, symbol, volume, price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.price = price

    @property
    def cost(self):
        return self.volume*self.price

    @property
    def fee(self):        
        return self.cost*self.BSC_BUY_FEE

    @property
    def total_cost(self):        
        return self.cost + self.fee

    def to_string(self):
        return f'{self.symbol} | Mua: {self.volume:,.0f} Giá: {self.price:,.0f} Phí (mua): {self.fee:,.0f} Tổng chi phí: {self.total_cost:,.0f}'
class SellOrder:
    BSC_SELL_FEE = 0.1/100
    BSC_SELL_TAX = 0.01/100

    def __init__(self, symbol,volume, price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.price = price        
    
    @property
    def income(self):
        return self.volume*self.price

    @property
    def fee(self):        
        return self.income*self.BSC_SELL_FEE
    
    @property
    def tax(self):        
        return self.income*self.BSC_SELL_TAX
    
    @property
    def total_income(self):        
        return self.income - self.tax - self.fee
    
    def to_string(self):        
        return f'{self.symbol} | Bán: {self.volume:,.0f} Giá: {self.price:,.0f} Thành tiền {self.income:,.0f} Phí (bán): {self.fee:,.0f} Thuế (bán): {self.fee:,.0f} Tổng thu: {self.total_income:,.0f}'

class Transaction:
    def __init__(self, symbol, volume, buy_price, sell_price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.b_order = BuyOrder(symbol=self.symbol,volume=self.volume, price=self.buy_price)
        self.s_order = SellOrder(symbol=self.symbol,volume=self.volume, price=self.sell_price)

    @property
    def profit(self):
        print(f'Bán: {self.s_order.total_income:,.0f}')
        print(f'Mua: {self.b_order.total_cost:,.0f}')
        profit = self.s_order.total_income - self.b_order.total_cost
        return profit

    @property
    def rate_profit(self):
        rate_profit = percent(self.b_order.total_cost, self.s_order.total_income)
        return rate_profit
        
    def to_string(self):
        return f'{self.symbol} | {self.volume:,.0f} Mua {self.buy_price} - Bán {self.sell_price} -> Lợi nhuận: {self.profit:,.0f} ({self.rate_profit:,.2f}(%))'

def test():
    order = BuyOrder(symbol="VND",volume=100,price=17500)
    print(order.to_string())

    s_order = SellOrder(symbol="KSB",volume=500,price=17350)
    print(s_order.to_string())

    t = Transaction(symbol='BSR',volume=2000,buy_price=17700, sell_price=17800)
    print(t.to_string())

test()