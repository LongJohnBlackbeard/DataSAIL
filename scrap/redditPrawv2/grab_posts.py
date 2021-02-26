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

        post_number = 0
        for post in new_posts:
            post_number += 1
            print(post_number)

            title = post.title.encode(encoding='UTF-8', errors='ignore')
            titleTwo = title.decode('UTF-8')

            post.comments.replace_more(limit=0)
            comments = ""
            for comment in post.comments.list():
                comments = comments + " " + comment.body

            title_and_comments = titleTwo + " " + comments

            body = post.selftext.encode(encoding='UTF-8', errors='ignore')
            bodyTwo = body.decode('UTF-8')
            body_and_title = title_and_comments + " " + bodyTwo
            " ".join(body_and_title.split())
            post_list.append(body_and_title)

            dateTest = post.created
            time_stamp_list.append(datetime.fromtimestamp(dateTest))
    df = pd.DataFrame({'timestamp': time_stamp_list, 'post title': post_list})
    return df
