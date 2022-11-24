from datetime import date, timedelta

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