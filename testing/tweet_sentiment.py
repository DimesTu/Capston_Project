from textblob import TextBlob

stock_index = "GOOG"
#stock_index = "ANZ.AX"
#stock_index = "FB"

tweet_start_date = '2017-10-02'
tweet_end_date = '2018-10-02'

file_name_tweets = 'stock_tweets/' + stock_index + '_' + tweet_start_date + '_' + tweet_end_date + '.txt'

with open(file_name_tweets, 'r') as f:
    text = f.read()

textblob = TextBlob(text)


#print("The sentiment index of the text is: \n", textblob.sentiment)
print("The polarity of the text is: \n", textblob.sentiment.polarity)
print("The subjectivity of the text is: \n", textblob.sentiment.subjectivity)






