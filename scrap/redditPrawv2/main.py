# Daniel Tujo
# DATASAIL
# Lewis University
# Main execution

from grab_posts import posts_and_timestamps
from create_instance import initiate_instance
import grab_posts
from datetime import datetime

startTime = datetime.now()

auth = initiate_instance()
reddit_input_list = grab_posts.subreddits()
current_day_data_frame = grab_posts.posts_and_timestamps(auth, reddit_input_list)

currentdate = datetime.now()
date = currentdate.date()
current_day_data_frame.to_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/daily_data_%s2.csv' % date, index=False)

print(datetime.now() - startTime)
