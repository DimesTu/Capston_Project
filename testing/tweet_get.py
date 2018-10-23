from TwitterAPI import TwitterAPI
from tweet_parser.tweet import Tweet
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import json

stock_index = "GOOG"
#stock_index = "ANZ.AX"
#stock_index = "FB"

#tweet_start_date = '2018-07-15'
tweet_start_date = '201801150000'           # UTC Timestamp

#tweet_end_date = '2018-10-12'
tweet_end_date = '201801160000'             # UTC Timestamp

#tweet_date = '201810150000'

tweet_number_per_page = 100 # range is 1-100
tweet_page_number = 15
tweet_number_max = tweet_number_per_page * tweet_page_number # max 1500

file_name_tweets = 'senti_tweets/' + stock_index + '_' + tweet_start_date + '_' + tweet_end_date + '.txt'
#print(file_name_tweets)

tweet_key_word = "google"

#consumer_key = data[1]
consumer_key = 'KzbAhJahqZ1oXLob5gik3Ay57'
#print(consumer_key)
#consumer_secret = data[3]
consumer_secret = 'AC29573TUDWLyRfLKsHP8oyGGiVzwydPcQihI8a6hLYttYihUa'
#print(consumer_secret)
#access_token = data[5]
access_token_key = '805364834107682816-aPi9PH2h8rsDKYbrbjw0k2ViU5Bjtjh'
#print(access_token)
#access_token_secret = data[7]
access_token_secret = 'CKhILlvFuedsNd5D5ADxWlZdQnFLYzOBeRWaV7eYbWdbI'
#print(access_token_secret)

"""
premium_search_args = load_credentials(".twitter_keys.yaml", account_type="premium")

rule = gen_rule_payload("google company") # testing with a sandbox account
print(rule)
"""

# TwitterAPI
# Create the API object
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
tweets = api.request('tweets/search/fullarchive/:EnvFull',
                     {'query': tweet_key_word,
                      'fromDate': tweet_start_date,
                      'toDate': tweet_end_date,
                      'maxResults': 50}).text
print(tweets)


"""
# Save to file
#with open('tweet.txt', 'r') as f:
    example = f.read()

print(example)
js = json(example)
print(js.text)

"""
