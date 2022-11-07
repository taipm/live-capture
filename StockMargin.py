class StockMargin:
    COMPANY = 'VPS'
    RATE_OF_YEAR = 13/100

    def __init__(self, amount) -> None:
        self.amout = amount

    @property
    def cost_in_day(self):
        pass