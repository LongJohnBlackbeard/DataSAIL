# Daniel Tujo
# Lewis University DataSAIL group
# Learning/Messing with Reddit API/PRAW
# PRAW is a wrapper/package used to help with reddit api interaction
# --note-- dont even know what a wrapper is.....

import praw
import sys
from sensitive import reddit_password  # credentials and stuff from another file #
from sensitive import reddit_username
from sensitive import client_id
from sensitive import client_secret
from sensitive import user_agent
from praw.models import MoreComments

reddit = praw.Reddit(client_id=client_id,  # this stuff here is what connects to #
                     client_secret=client_secret,  # reddit api using OAUTH credentials  #
                     password=reddit_password,  # I have another file containing the  #
                     user_agent=user_agent,  # info here because this file is on   #
                     username=reddit_username)  # github

subredditInput = input("What subreddit do you want to search? ")  # asks input for what subreddit to search
# you can search all of reddit by typing "all"

sys.stdout = open("redditScraping.txt", "w")    # starts process of exporting the output to a textfile

hot_posts = reddit.subreddit(subredditInput).hot(limit=5)         # variable assignment that has top 5 posts from the
for post in hot_posts:                                            # subreddit input
    print("*" * 75)           # loops through each post from the 5 posts grabbed
    print(post.title)         # posts the title
    submission = reddit.submission(post)
    # submission.comments.replace_more(limit=0)

    index = 0                 # start of a counter to limit post comments
    for top_level_comment in submission.comments:    # this loop is inside the previous loop
        index += 1                                   # this loop grab the top comment in the post
        if index == 6:                               # with the counter, it grabs 5 comments
            break
        print("-" * 75)
        print(index, "-", top_level_comment.body.encode('cp1252', errors='ignore'))

sys.stdout.close()
