import numpy as np

class AnalysisList:
    '''
    lst: list of number as float, int, decimail, ...
    '''
    def __init__(self, lst:list) -> None:
        self.items = lst
        self.max = np.max(lst)
        self.min = np.min(lst)
        self.avg = np.average(lst)
        self.first = lst[0]
        self.last = lst[len(self.items)-1]
        self.sum = np.sum(lst)
    
    def pct(self, min, max):
        '''
        min -> x% = max
        '''
        return ((max-min)/min)*100

    def distance(self, from_index=-1):
        min = self.min
        if from_index >=0:
            min = np.min(self.items[0:from_index])
        return self.pct(min=min,max=self.max)

    def __len__(self):
        return len(self.items)
    
    def __str__(self) -> str:
        return f'Items length: {self.__len__()}'+\
            f'\nFirst: {self.first:,.2f} - Last: {self.last:,.2f}'+\
            f'\nSum: {self.sum:,.2f} - Max: {self.max:,.2f} - Min: {self.min:,.2f} - Avg: {self.avg:,.2f}'+\
                f'\nd({self.__len__()}): {self.distance(from_index=-1):,.2f} - ({self.distance(from_index= 10):,.2f})'

# a = AnalysisList([1,2,3,4,5])
# print(a)