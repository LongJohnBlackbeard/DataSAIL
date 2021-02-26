import pandas as pd
import requests
from pandas import DataFrame

df = pd.read_csv("tickers.csv")
ticker_list = df['DDD'].to_list()


ticker_list_with_sign = []
ticker_name = []


def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


for i in ticker_list:
    temp_list = ["$", i]
    ticker_string = "".join(temp_list)
    ticker_list_with_sign.append(ticker_string)
    company = get_symbol(i)
    print(company)
    ticker_name.append(company)

f = open("tickertext", "a")
f.write(ticker_list)
f.write(ticker_list_with_sign)
f.close()

# df = pd.DataFrame({'Ticker': ticker_list, '$Ticker': ticker_list_with_sign, 'Company Name': ticker_name})
# df.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\tickertable.csv', index=False)



