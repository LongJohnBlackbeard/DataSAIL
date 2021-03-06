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

currentDate = datetime.now()
date = currentDate.date()
current_day_data_frame.to_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/daily_data_%s.csv' % date, index=False)
# current_day_data_frame.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\daily_data_%s.csv' % date, index=False)

print(datetime.now() - startTime)

print(datetime.now)
