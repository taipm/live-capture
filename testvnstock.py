from vnstock import *

# lst = listing_companies()
# print(lst)

# x = price_board('TCB,SSI,VND')
# print(x)

df =  stock_intraday_data(symbol='hax', 
                            page_num=0, 
                            page_size=5000)
print(df.head(20))