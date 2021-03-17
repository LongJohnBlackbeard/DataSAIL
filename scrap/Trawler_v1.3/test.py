import reddit_instance
import pandas as pd

reddit = reddit_instance.initiate_instance()
new_posts = reddit.subreddit("stocks").new(limit=10)
print(type(new_posts))
print(new_posts)

df = pd.DataFrame(new_posts)
print(df)
