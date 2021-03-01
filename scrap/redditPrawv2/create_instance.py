# Create Reddit Instance

import praw
from sensitive import reddit_password
from sensitive import reddit_username
from sensitive import client_id
from sensitive import client_secret
from sensitive import user_agent
from datetime import datetime


def initiate_instance():
    reddit = praw.Reddit(client_id=client_id,          # this stuff here is what connects to #
                         client_secret=client_secret,  # reddit api using OAUTH credentials  #
                         user_agent=user_agent)        # I have another file containing the  #
                                                       # info here because this file is on
    return reddit