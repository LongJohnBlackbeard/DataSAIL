import praw

from sensitive import reddit_password
from sensitive import reddit_username
from sensitive import client_id
from sensitive import client_secret
from sensitive import user_agent
from datetime import datetime


def initiate_instance():
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         user_agent=user_agent)
    return reddit
