class Pivot:
    def __init__(self, symbol, index) -> None:
        self.symbol = symbol.upper()
        self.index = index
    
    def to_string(self):
        return f'{self.symbol} - {self.index}'
