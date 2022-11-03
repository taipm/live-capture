def inc_percent(x, p):
    '''
    p: Phần trăm (nếu 3% thì p = 3)
    '''
    return x + (p/100)*x

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

#print(RichNumber(77.4).rich_text)

    