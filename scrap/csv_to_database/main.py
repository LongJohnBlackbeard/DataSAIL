import os

directory = r'/home/dtujo/myoptane/Trawler/Dataframes'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        print(os.path.join(directory, filename))
    else:
        continue
