import praw
from sensitive import reddit_password
from sensitive import reddit_username
from sensitive import client_id
from sensitive import client_secret
from sensitive import user_agent
from datetime import datetime

import grab_posts
import reddit_instance

auth = reddit_instance.initiate_instance()

reddit_input_list = grab_posts.subreddits()
grab_posts.post_and_timestamps(auth, reddit_input_list)
