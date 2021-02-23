# Daniel Tujo
# Lewis University DataSAIL group
# Learning/Messing with Reddit API/PRAW
# PRAW is a wrapper/package used to help with reddit api interaction
# --note-- dont even know what a wrapper is.....

import praw
import sys
import pandas as pd
from pandas import DataFrame
import csv

from sensitive import reddit_password  # credentials and stuff from another file #
from sensitive import reddit_username
from sensitive import client_id
from sensitive import client_secret
from sensitive import user_agent
from datetime import datetime
from praw.models import MoreComments

reddit = praw.Reddit(client_id=client_id,  # this stuff here is what connects to #
                     client_secret=client_secret,  # reddit api using OAUTH credentials  #
                     password=reddit_password,  # I have another file containing the  #
                     user_agent=user_agent,  # info here because this file is on   #
                     username=reddit_username)  # github

postList = []
timeStampList = []

condition = False
reddit_input_list = []
while not condition:  # Added ability to enter multiple subreddits
    reddit_input = input("What subreddit do you want to search? Press Enter to finish. ")
    if reddit_input == "":
        break
    else:
        reddit_input_list.append(reddit_input)


for subreddit in reddit_input_list:                                   # Iterates through every subreddit entered
    hot_posts = reddit.subreddit(subreddit).new(limit=None)
    for post in hot_posts:                                            # iterates through every post grabbed in subreddit
        string = post.title.encode(encoding='UTF-8', errors='ignore')
        stringTwo = string.decode('utf-8')  # appends post and timestamp into perspective list
        postList.append(stringTwo)
        dateTest = post.created
        timeStampList.append(datetime.fromtimestamp(dateTest))

df = pd.DataFrame({'timestamp': timeStampList, 'post title': postList})         # adds timestamp list and post list to
df.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\new.csv', index=False)             # a dataframe and exports
