from datetime import date, timedelta


class VnDate:
    def __init__(self, _date:date) -> None:
        self.currentDate = _date
        self.today = date.today()
    @property
    def isWeekend(self):
        index = self.currentDate.weekday()
        if index in [5,6]:
            return True
        return False
            
    @property
    def next(self):
        value = self.currentDate
        value += timedelta(days=1)
        return value

    @property    
    def previous(self):
        value = self.currentDate
        value += timedelta(days=-1)
        return value
    
    def __str__(self) -> str:
        return f'{self.currentDate.strftime("%Y-%m-%d")} - {self.today}'

def Test_VnDate():
    v = VnDate(_date=date(2002,10,1))
    print(v)
    print(v.next)
    print(v.previous)
    print(f'Weekend: {v.isWeekend}')
#Test_VnDate()