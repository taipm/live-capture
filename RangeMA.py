class RangeMA:
    def __init__(self, number:float) -> None:
        self.number = number
        self.max = number + number*0.5/100
        self.min = number - number*0.5/100
        self.distance = (self.max - self.min)/self.min    

    def isIn(self, number:float):
        if number >= self.min and number <= self.max:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f'{self.min:,.2f} -> {self.number:,.2f} -> {self.max:,.2f} : d = {self.distance:,.2f}'


def Test_RangeMA():
    r = RangeMA(number=16.25)
    print(r)
    values = [16,16.05,16.1,17,16.26]
    for v in values:
        print(f'\nIs in : {v} - {r.isIn(v)}')

#Test_RangeMA()