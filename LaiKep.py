def CompoundingInterest(amount, rate, rountines):
    amount = amount
    for i in range(0, rountines):
        amount += amount*rate
    return amount

# x = CompoundingInterest(amount=100000000, rate=3/100, rountines=10)
# print(f'{x:,.2f}')