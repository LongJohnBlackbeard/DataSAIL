import csv

import findCounts
import grabPosts
import redditInstance
import pandas as pd

auth = redditInstance.initiate_instance()

dataDF = grabPosts.post_and_timestamps(auth, grabPosts.reddit_input_lists)

data = ''.join(dataDF['Post/Comment'].values())

result = findCounts.process_bodies(data)

result = findCounts.filter_pos_tokens(result, findCounts.target_pos_tags)

result = findCounts.count_tickers(result, findCounts.tickers)

resultDF = pd.DataFrame(result)
print(result)

resultDF.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\testing.csv', index=False)