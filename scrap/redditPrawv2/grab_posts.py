# Grab Posts and times

import praw
from create_instance import initiate_instance
import datetime
from datetime import datetime
import pandas as pd


# Asks user for what subreddits to search
def subreddits():
    reddit_input_list = []
    condition = False

    while not condition:
        reddit_input = input("What subreddit do you want to search? Press Enter to finish. ")

        if reddit_input == "":
            break
        else:
            reddit_input_list.append(reddit_input)

    return reddit_input_list


def posts_and_timestamps(reddit, subreddit_list):
    post_list = []
    time_stamp_list = []

    for subreddit in subreddit_list:
        new_posts = reddit.subreddit(subreddit).new(limit=None)

        for post in new_posts:
            string = post.title.encode(encoding='UTF-8', errors='ignore')
            stringTwo = string.decode('utf-8')
            post_list.append(stringTwo)
            dateTest = post.created
            time_stamp_list.append(datetime.fromtimestamp(dateTest))
    df = pd.DataFrame({'timestamp': time_stamp_list, 'post title': post_list})
    return df
