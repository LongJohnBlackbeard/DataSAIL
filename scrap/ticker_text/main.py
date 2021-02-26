import pandas as pd
from pandas import DataFrame

df = pd.read_csv("tickertable.csv")

ticker_list = df["Ticker"].to_list()

ticker_list_with_sign = df["$Ticker"].to_list()

ticker_name = df["Company Name"].to_list()

f = open("tickertext", "a")

for ticker in ticker_list:
    f.write(ticker + "\n")

for ticker in ticker_list_with_sign:
    f.write(ticker + "\n")

for name in ticker_name:
    f.write(str(name) + "\n")

f.close()
