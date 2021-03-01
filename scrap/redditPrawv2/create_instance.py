# Create Reddit Instance

import praw
from sensitive import reddit_password
from sensitive import reddit_username
from sensitive import client_id
from sensitive import client_secret
from sensitive import user_agent
from datetime import datetime


def initiate_instance():
    reddit = praw.Reddit(client_id=client_id,  # this stuff here is what connects to #
                         client_secret=client_secret,  # reddit api using OAUTH credentials  #
                         password=reddit_password,  # I have another file containing the  #
                         user_agent=user_agent,  # info here because this file is on   #
                         username=reddit_username)
    return reddit
