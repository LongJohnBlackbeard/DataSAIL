# author: Alexander DeForge
# date: 03/06/2021
# purpose: convert tickertable.csv data and wsbData.json into a table containing (Ticker name, Created, Count).
#           Where tickertable.csv entries are identifiers for publicly traded companies on the United States stock market and
#           wsbData.json is historical data containing posts and other data from the subreddit /r/wallstreetbets.
#           Ticker name is a stock name (e.g. APPL), Created is a datetime object identifying the day (year, month, day) a tickertable.csv entry was found in a post body
#           from wsbData.json and Count is the number of times a tickertable.csv entry was found in a post body from wsbData.json on a given day.
# organization: Lewis University DataSAIL, Dr. Szczurek, Spring 2021
# version: 2
VERSION = 2


import dask
import dask.dataframe as dd
from datetime import datetime
import numpy as np
import pandas as pd
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import big_historical_v2_cython as helper


def main(PARTITIONS, MODIFIER):
    # constants for tickertable.csv
    TICKER_FILENAME = "tickertable.csv"
    COMPANY_NAME_HEADER = "Company Name"
    TICKER_NAME_HEADER = "Ticker"
    # constants for wsbData.json
    WSBDATA_FILENAME = "wsbData.json"
    BODY = "body"
    CREATED_UTC = "created_utc"


    # tokenize, pos tag company names, extract all unique pos tags
    def extract_target_pos_tags(target):
        tokenizer = word_tokenize
        tagger = pos_tag
        result = {y[1] for x in target for y in tagger(tokenizer(x))}
        return list(result)

    # tokenize, pos tag company names
    def extract_target_pos_tokens(target):
        tokenizer = word_tokenize
        tagger = pos_tag
        result = [tagger(tokenizer(x)) for x in target]
        return result

    # convert utc epoch time to datetime object
    def format_time(arg):
        dt = datetime.fromtimestamp(arg)
        return datetime(dt.year, dt.month, dt.day)

    # tokenize and pos tag corpus
    def process_bodies(body):
        tokenize = word_tokenize
        tag = pos_tag
        result = tokenize(body)
        result = tag(result)
        result = [(x[0].lower(), x[1]) for x in result]
        return result


    start = datetime.now()
    print("Starting")
    print(start)
    # load tickertable.csv data
    ticker_df = pd.read_csv(TICKER_FILENAME)
    ticker_df = ticker_df[[TICKER_NAME_HEADER,COMPANY_NAME_HEADER]]
    # if a tickertable.csv entry has an empty string in a column, that means
    #  the stock is not traded (as of when tickertable.csv was populated, 2021)
    ticker_df.replace('', np.nan, inplace=True)
    ticker_df.dropna(inplace=True)
    # the pos tags related to the Ticker names
    target_pos_tags = ['NNP', 'NNS', 'NN', 'CD']
    # the Ticker names will be used to match occurrences in the corpora
    tickers = ticker_df[TICKER_NAME_HEADER].tolist()

    # load wsbData.json data
    result = pd.read_json(WSBDATA_FILENAME, lines=True)
    result = result[[CREATED_UTC,BODY]]
    # remove empty entries
    result.replace('',np.nan,inplace=True)
    result.dropna(inplace=True)
    # convert to dask dataframe
    wsb_df = dd.from_pandas(result, npartitions=PARTITIONS)
    # convert utc epoch time to a datetime object with day granularity
    wsb_df[CREATED_UTC] = wsb_df[CREATED_UTC].map(lambda x: format_time(x)).compute()
    # pivot on day with body aggregation
    result = wsb_df.groupby(by=[CREATED_UTC])[BODY].apply(lambda x: helper.aggregate_bodies(x.tolist()), meta=pd.Series(dtype='object'))
    # tokenize and pos tag bodies
    result = result.map_partitions(lambda df: df.map(lambda x: process_bodies(x)), meta=pd.Series(dtype='object'))
    # filter pos tagged corpus with respect to NNP, NNS, NN and CD tags
    result = result.map_partitions(lambda df: df.map(lambda x: helper.process_pos_tokens(x,target_pos_tags)), meta=pd.Series(dtype='object'))
    # analysis
    # parse pos-tokenized-and-filtered corpora with respect to Tickers, for occurrences
    result = result.map_partitions(lambda df: df.map(lambda x: helper.parse_tickers(x,tickers)), meta=pd.Series(dtype='object'))
    # compute
    wsb_df = result.compute()
    end = datetime.now()
    print(end)


    # munge final dataframe
    final_df = pd.DataFrame(wsb_df.tolist(), index=wsb_df.index)
    print(final_df.head())


    # base filename
    timestamp = str(datetime.now())
    filename = timestamp + "_big_historical_v" + str(VERSION) + "_" + MODIFIER


    # save elapsed time to a file
    elapsed_filename = filename + "_elapsed.txt"
    with open(elapsed_filename, 'a') as f:
        f.write("Start: " + str(start) + "\n")
        f.write("End: " + str(end) + "\n")
        f.write(str(final_df.head(10)))

    final_data_filename = filename + "_data.csv"
    final_df.to_csv(final_data_filename)
    print("Done.")


if __name__ == "__main__":
    MODIFIER = "tickers_only"
    PARTITIONS = 28
    dask.config.set(scheduler="processes", num_workers=28)
    main(PARTITIONS, MODIFIER)
