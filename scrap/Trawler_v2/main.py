import csv

import findCounts
import grabPosts
import redditInstance

auth = redditInstance.initiate_instance()

data = grabPosts.post_and_timestamps(auth, grabPosts.reddit_input_lists)

result = findCounts.process_bodies(data['Post/Comment'])

result = findCounts.filter_pos_tokens(result, findCounts.target_pos_tags)

result = findCounts.count_tickers(result, findCounts.tickers)

with open("data.csv", "w", newline="") as csv_file:
    cols = ["ticker", "occurrences"]
    writer = csv.DictWriter(csv_file, fieldnames=cols)
    writer.writeheader()
    writer.writerow(result)
