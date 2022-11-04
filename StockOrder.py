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