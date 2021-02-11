import pandas as pd

df = pd.read_csv("tickers.csv")
ticker_list = df['DDD'].to_list()
print(ticker_list)

amount = 0
for i in ticker_list:
    amount += 1

print(amount)