from datetime import date, timedelta
class VnDate:
    format_date = "%Y-%m-%d"
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
        return f'{self.currentDate.strftime(self.format_date)} - {self.today}'
