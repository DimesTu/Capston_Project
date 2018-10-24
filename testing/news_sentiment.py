from textblob import TextBlob
from datetime import datetime, timedelta
import pandas as pd

# Set stock index
stock_index = "GOOG"
#stock_index = "ANZ.AX"
#stock_index = "FB"

# Set the start and end date of news available. These are strings
news_start_date = '2016-07-01'
news_end_date = '2018-10-12'         # Only 1 month max interval for newsapi, but full archieve for nytimes
news_current_date = news_start_date

# Parse the string date into datetime object. These are datetime object
news_start_datetime = datetime.strptime(news_start_date, '%Y-%m-%d')
#print(start_datetime)
news_end_datetime = datetime.strptime(news_end_date, '%Y-%m-%d')
news_current_datetime = datetime.strptime(news_current_date, '%Y-%m-%d')
#print((end_datetime - start_datetime).days)

# Set the file names read from raw and (news or tweets), after sentiment, write to senti
file_name_raw = 'stock_data_raw/' + stock_index + '.csv'
#file_name_tweets = 'senti_tweets/' + stock_index + '_' + tweet_start_date + '_' + tweet_end_date + '.txt'
file_name_senti = 'stock_data_senti/' + stock_index + '.csv'

# Read from raw
data_senti = pd.read_csv(file_name_raw, header=0)
data_senti = data_senti.set_index('Date')
data_senti['Pola'] = 0
data_senti['Subj'] = 0.5
#print(data_senti)

# To store the sentiment result into another file
for i in range((news_end_datetime - news_start_datetime).days + 1) :
    #print('Now, i is', i)
    if (news_current_date in data_senti.index) :
        file_name_news = 'senti_news/' + stock_index + '_' + news_current_date + '.txt'
        with open(file_name_news, 'r') as f:
            text = f.read()
        textblob = TextBlob(text)
        data_senti.loc[news_current_date, ['Pola', 'Subj']] = [textblob.polarity, textblob.subjectivity]

    news_current_datetime = news_current_datetime + timedelta(days=1)
    news_current_date = datetime.strftime(news_current_datetime, '%Y-%m-%d')


print(data_senti)
data_senti.to_csv(file_name_senti, header=True, index=True, float_format='%.6f')







