# Daniel Tujo
# Lewis University DataSAIL group
# Learning/Messing with Reddit API/PRAW
# PRAW is a wrapper used to help grab data from reddit
# --note-- dont even know what a wrapper is.....

import praw
import sys
from sensitive import reddit_password
from sensitive import reddit_username
from sensitive import client_id
from sensitive import client_secret
from sensitive import user_agent
from praw.models import MoreComments

reddit = praw.Reddit(client_id= client_id,
                     client_secret= client_secret,
                     password= reddit_password,
                     user_agent= user_agent,
                     username= reddit_username)

subredditInput = input("What subreddit do you want to search? ")

sys.stdout = open("redditScraping.txt", "w")

hot_posts = reddit.subreddit(subredditInput).hot(limit=5)
for post in hot_posts:
    print("*" * 75)
    print(post.title)
    submission = reddit.submission(post)
    # submission.comments.replace_more(limit=0)

    index = 0
    for top_level_comment in submission.comments:
        index += 1
        if index == 6:
            break
        print("-" * 75)
        print(index, "-", top_level_comment.body.encode('cp1252', errors='ignore'))

sys.stdout.close()

