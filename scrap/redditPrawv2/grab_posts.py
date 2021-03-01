# Grab Posts and times

import praw
from create_instance import initiate_instance
import datetime
from datetime import datetime
import pandas as pd
from create_instance import initiate_instance
import time

# Asks user for what subreddits to search
# csv_file_name = input("What is the exact name of the csv file?")
# data = pd.read_csv('/home/dtujo/myoptane/Trawler/Dataframes/%s' % csv_file_name)

# data = pd.read_csv('D:\Git\lewisuDataSAIL\Dataframes\%s' % csv_file_name)
# old_posts_list = data['post title'].tolist()
# print(old_posts_list)
last_unix_timestamp = int(input("What was the last unix timestamp of that last post/comment? "))

auth = initiate_instance()
rate_limit = auth.auth.limits


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

        post_number = 0
        for post in new_posts:
            post_number += 1
            print("post" + str(post_number))
            print(rate_limit)

            if post.created > last_unix_timestamp:
                post_number += 1
                print("grabbed post " + str(post_number))
                print(post.title)
                print(rate_limit)

                title = post.title.encode(encoding='UTF-8', errors='ignore')
                titleTwo = title.decode('UTF-8')

                body = post.selftext.encode(encoding='UTF-8', errors='ignore')
                bodyTwo = body.decode('UTF-8')

                body_title = titleTwo + " " + bodyTwo

                post_list.append(body_title)
                dateTest = post.created
                time_stamp_list.append(datetime.fromtimestamp(dateTest))
            else:
                print("skipped")
                print(post.title)

            while True:
                try:
                    post.comments.replace_more(limit=50)
                    break
                except Exception:
                    time.sleep(1)

            for comment in post.comments.list():
                if comment.created_utc > last_unix_timestamp:

                    print(rate_limit)
                    post_number += 1
                    print("grabbed comment " + str(post_number))
                    print(comment)
                    post_list.append(comment.body)
                    dateComment = comment.created_utc
                    time_stamp_list.append(datetime.fromtimestamp(dateComment))
                else:
                    print("skipped")
                    print(comment.body)

    df = pd.DataFrame({'timestamp': time_stamp_list, 'post title': post_list})
    return df
