class StockChart:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.imageUrl = f'https://vip.cophieu68.vn/imagechart/sma50/{self.symbol.lower()}.png'

    # def getEmbedChart(self):
    #     #src="https://www.cophieu68.vn/chartsymbol_chart.php?screenwidth=3360&amp;csc=1669222800&amp;s=2021-11-24&amp;e=2022-11-24&amp;page=0&amp;m=candle&amp;dateby=1&amp;extend_height=1&amp;extend_weight=1&amp;data_type1=1&amp;data_type2=&amp;sma=1&amp;sma_day=20&amp;sma2_day=&amp;sma3_day=&amp;sma4_day=&amp;chartsize=1&amp;id=hpg&amp;time=1669272096"
    #     src = f'<img src="https://www.cophieu68.vn/chartsymbol_chart.php?screenwidth=3360&amp;csc=1669222800&amp;s=2021-11-24&amp;e=2022-11-24&amp;page=0&amp;m=candle&amp;dateby=1&amp;extend_height=1&amp;extend_weight=1&amp;data_type1=1&amp;data_type2=&amp;sma=1&amp;sma_day=20&amp;sma2_day=&amp;sma3_day=&amp;sma4_day=&amp;chartsize=1&amp;id=hpg&amp;time=1669272096" alt="" title="" border="0">'
    #     return src