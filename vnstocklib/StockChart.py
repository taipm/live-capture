class StockChart:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.imageUrl = f'https://vip.cophieu68.vn/imagechart/sma50/{self.symbol.lower()}.png'
        self.dailyChartUrl = f'https://vip.cophieu68.vn/imagechart/candle/{self.symbol.lower()}.png'
        self.weeklyChartUrl = f'https://vip.cophieu68.vn/imagechart/candleweek/{self.symbol.lower()}.png'