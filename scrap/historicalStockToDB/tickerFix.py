
import pandas as pd
import csv

tickerCSV = pd.read_csv('tickertable.csv')

print(tickerCSV.loc[pd.notnull(tickerCSV["Company Name"])])
tickerCSV = (tickerCSV.loc[pd.notnull(tickerCSV["Company Name"])])

tickerCSV.to_csv(r'FinalTickerTable.csv')



