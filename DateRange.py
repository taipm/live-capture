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

class DateRange:
    def __init__(self, start_date, end_date):
        self.startDate = start_date
        self.endDate = end_date
        self.length = end_date-start_date

        self.current = self.startDate

    def __iter__(self):
        current_day = self.startDate
        while current_day < self.endDate:
            yield current_day
            current_day += timedelta(days = 1)

    def __next__(self, step):
        value = self.current
        self.current += timedelta(days=step)
        return self.current

    def isInRange(self, date:date):
        '''
        meaning: []
        '''
        if date >= self.startDate and date <= self.endDate:
            return True
        return False


def Test_DateRange():
    r = DateRange(start_date=date(2022,10,1), end_date= date(2022,10,20))
    print(r.startDate)
    print(r.length)
    print(r.isInRange(date=date(2022,10,15)))
    print(r.isInRange(date=date(2022,10,25)))
    #print(next(r,step=2))
    print(r.__next__(step=2))

Test_DateRange()
Test_VnDate()