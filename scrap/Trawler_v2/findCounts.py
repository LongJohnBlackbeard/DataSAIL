import nltk
import pandas as pd

from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# constants for tickertable.csv
TICKER_FILENAME = "newTickerList.csv"
COMPANY_NAME_HEADER = "Company Name"
TICKER_NAME_HEADER = "Ticker"

# load tickertable.csv to get ticker names
ticker_df = pd.read_csv(TICKER_FILENAME)
ticker_df = ticker_df[[TICKER_NAME_HEADER]]

# setup for later
target_pos_tags = ['NNP', 'NNS', 'NN', 'CD']
tickers = ticker_df[TICKER_NAME_HEADER].tolist()

for ticker in tickers:
    if ("." in ticker) or ("-" in ticker):
        tickers.remove(ticker)


# tokenize and pos tag a raw body, where a raw body is a day's worth of posts/comments
def process_bodies(raw_body):
    tokenize = word_tokenize
    tag = pos_tag
    result = tokenize(raw_body)
    result = tag(result)
    result = [(x[0].lower(), x[1]) for x in result]
    return result


# filter the corpus, where a corpus is a day's worth of processed posts/comments
def filter_pos_tokens(tagged_corpus, target_pos_tags):
    result = []
    for pos_token in tagged_corpus:
        # if the part of speech is one of the target parts of speech, keep it
        if pos_token[1] in target_pos_tags:
            result.append(pos_token)
    return result


# extract occurrences for each ticker
def count_tickers(tagged_corpus, tickers):
    occurrences = 0
    result = {}
    for ticker in tickers:
        occurrences = 0
        for pos_token in tagged_corpus:
            # if the ticker matches the token value, count it
            if ticker.lower() == pos_token[0].lower():
                occurrences = occurrences + 1
    result[ticker] = occurrences
    return result


# # raw_body is the posts/comments for a day's worth of data
# result = process_bodies(raw_body)
# # target_pos_tags is given
# result = filter_pos_tokens(result, target_pos_tags)
# # tickers is given
# result = count_tickers(result, tickers)
# # the end result is a dictionary of {key: vallue} such that {ticker: occurrencces}
# result
