import requests
from newsapi import NewsApiClient
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import time

from dateutil.parser import parse

# Set parameters
news_api_type = 'everything'
#news_api_type = 'top-headlines'
#news_api_type = 'sources'

news_country = 'us'
#news_category = 'business'
news_category = 'technology'
news_source = 'the-wall-street-journal'
key_words = 'google'
#start_date = '2016-07-01'
start_date = '2018-10-03'
end_date = '2018-10-12'         # Only 1 month max interval for newsapi, but full archieve for nytimes
current_date = start_date
newsapi_ApiKey = '443b379064a7437abceec0b03e215f72'
nytimes_Apikey = '5e1e5a95697145acaeb0b1c2445d2efd'

sort_by = 'popularity'

stock_index = "GOOG"


# Parse the string date into datetime object
start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
#print(start_datetime)
end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
current_datetime = datetime.strptime(current_date, '%Y-%m-%d')
#print((end_datetime - start_datetime).days)


# Set apply the api key
#api = NewsApiClient(api_key=my_api_key)

# Start loop from start_date to end_date
for j in range((end_datetime - start_datetime).days + 1):
#for j in range(1) :
    print(current_date)

    """
    # Define the url of Newsapi
    url = ('https://newsapi.org/v2/' +
           news_api_type +
           '?q=' + key_words +
           '&language=en' +
           #'&sources=' + news_source +        # source can't be mixed with country or category
           #'&country=' + news_country +        # country can't be mixed with source
           #'&category=' + news_category +       # category can't be mixed with source
           '&from=' + current_date +
           '&to=' + current_date +
           '&sortBy=' + sort_by +
           '&apiKey=' + newsapi_ApiKey
           )
    """

    # Define the url of Times News
    current_datetime = current_datetime + timedelta(days=1)
    next_datetime = current_datetime
    next_date = datetime.strftime(next_datetime, '%Y-%m-%d')
    # url = ('https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=5e1e5a95697145acaeb0b1c2445d2efd&q=google&begin_date=20180101&end_date=20180201')
    url = ('https://api.nytimes.com/svc/search/v2/articlesearch.json'
           + '?api-key=' + nytimes_Apikey
           + '&q=' + key_words
           + '&begin_date=' + current_date
           + '&end_date=' + next_date
           )
    print(url)

    # To get request JSON object from url API
    response = requests.get(url).text

    # This is for testing rather than get real API
    #with open('senti_news/test1.txt', 'r') as f:
    #    response = f.read()

    #print(response)

    result = json.loads(response)
    #number_of_news = result['response']['meta']['hits']
    number_of_news = len(result['response']['docs'])
    if number_of_news >= 2 :
        number_of_news = 2

    print(number_of_news)
    # Write the snippet,
    news_file_name = 'senti_news/' + stock_index + '_' + current_date + '.txt'
    #news_file_name = 'senti_news/test3.txt'

    with open(news_file_name, 'w+') as f:
        f.write('Date: ' + current_date + '\n')

    for i in range(number_of_news):
        #print(result['response']['docs'][i]['snippet'])
        # total_news_number = int(result['totalResults'])
        with open(news_file_name, 'a+') as f:
            if 'snippet' in result['response']['docs'][i]:
                text = result['response']['docs'][i]['snippet']
            else :
                text = 'None\n'
            f.write(str(text) + '\n')
            if 'abstract' in result['response']['docs'][i]:
                text = result['response']['docs'][i]['abstract']
            else :
                text = 'None\n'
            f.write(str(text) + '\n')
            if 'main' in result['response']['docs'][i]['headline']:
                text = result['response']['docs'][i]['headline']['main']
            else:
                text = 'None\n'
            f.write(str(text) + '\n')
            if 'kicker' in result['response']['docs'][i]['headline']:
                text = result['response']['docs'][i]['headline']['kicker']
            else :
                text = 'None\n'
            f.write(str(text) + '\n')
            if 'content_kicker' in result['response']['docs'][i]['headline']:
                text = result['response']['docs'][i]['headline']['content_kicker']
            else :
                text = 'None\n'
            f.write(str(text) + '\n')
            if 'print_headline' in result['response']['docs'][i]['headline']:
                text = result['response']['docs'][i]['headline']['print_headline']
            else :
                text = 'None\n'
            f.write(str(text) + '\n\n')



    # add 1 day of current datetime object, and then back to string

    # To wait 1s as API calling limit
    current_date = next_date
    #time.sleep(1)
    #exit()











