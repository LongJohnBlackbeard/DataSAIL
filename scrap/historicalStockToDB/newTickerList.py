import csv
import pandas as pd

# with open('NYSE.txt') as f:
#     reader = csv.reader(f, delimiter="\t")
#     d = list(reader)
# print(reader)

dataset = pd.read_csv('NYSE.txt', delimiter="\t")
print(dataset)

dataset.to_csv(r'newTickerList.csv')

