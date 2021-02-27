# Will import previous day's csv to compare data with current days data

import pandas as pd


def old_post_list():
    csv_file_name = input("What is the exact name of the csv file?")
    data = pd.read_csv('/home/dtujo/myoptane/Trawler/Dataframes/%s' % csv_file_name)
    posts_list = data['post title'].tolist()
    return posts_list
