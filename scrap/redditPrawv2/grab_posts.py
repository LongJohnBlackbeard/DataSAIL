# Grab Posts and times

import praw
from create_instance import initiate_instance
import datetime
from datetime import datetime
import pandas as pd

# Asks user for what subreddits to search
# csv_file_name = input("What is the exact name of the csv file?")
# data = pd.read_csv('/home/dtujo/myoptane/Trawler/Dataframes/%s' % csv_file_name)

# data = pd.read_csv('D:\Git\lewisuDataSAIL\Dataframes\%s' % csv_file_name)
# old_posts_list = data['post title'].tolist()
# print(old_posts_list)
last_unix_timestamp = int(input("What was the last unix timestamp of that last post/comment? "))


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
            print(post_number)
            if post.created > last_unix_timestamp:
                post_number += 1
                print(post_number)

                title = post.title.encode(encoding='UTF-8', errors='ignore')
                titleTwo = title.decode('UTF-8')

                body = post.selftext.encode(encoding='UTF-8', errors='ignore')
                bodyTwo = body.decode('UTF-8')

                post_list.append(titleTwo)
                dateTest = post.created
                time_stamp_list.append(datetime.fromtimestamp(dateTest))

                post_list.append(bodyTwo)
                dateTest = post.created
                time_stamp_list.append(datetime.fromtimestamp(dateTest))

            post.comments.replace_more(limit=None)
            for comment in post.comments.list():
                post_number += 1
                print(post_number)
                if comment.created_utc > last_unix_timestamp:
                    post_number += 1
                    print(post_number)
                    print(comment.body)
                    post_list.append(comment.body)
                    dateComment = comment.created_utc
                    time_stamp_list.append(datetime.fromtimestamp(dateComment))

    df = pd.DataFrame({'timestamp': time_stamp_list, 'post title': post_list})
    return df
