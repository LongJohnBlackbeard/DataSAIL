import pandas as pd

df = pd.read_csv("tickers.csv")
ticker_list = df['DDD'].to_list()
# print(ticker_list)



ticker_list_with_sign = []
for i in ticker_list:
    ticker_list_with_sign.append(i)
    temp_list = ["$", i]
    ticker_string = "".join(temp_list)
    ticker_list_with_sign.append(ticker_string)


print(ticker_list_with_sign)

amount = 0
for i in ticker_list_with_sign:
    amount += 1

print(amount)
