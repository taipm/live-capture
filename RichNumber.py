import math
from Constant import *
from Caculator import *
from DateHelper import *

class RichNumber:
    def __init__(self, x) -> None:
        self.x = float(x)
        self.rich_text = self.rich_info()

    def rich_info(self):
        steps = [-15,-10,-5,3,5,7,10,15]
        output = ''
        for i in steps:
            output += f'\n{i} (%) : {inc_percent(self.x,i):,.2f}'
        return output
    
    def toText(self):
        text = ''
        signal = ''
        number = 0
        if self.x < 0:
            signal = '-'
            number = math.fabs(self.x)
        else:
            number = self.x

        if(number > billion):
            text = f'{number/billion:,.2f} B'
        elif(number < billion and number >= million):
            text = f'{number/million:,.2f} M'
        elif(number < million and number >= thousand):
            text = f'{number/thousand:,.2f} K'
        else:
            text = f'{number}'
        return signal + text
    