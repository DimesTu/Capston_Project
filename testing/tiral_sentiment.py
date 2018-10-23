from textblob import TextBlob

text1 = "Date: 2018-09-12"

with open('senti_news/test2.txt', 'r') as news_file1:
    news1 = news_file1.read()

with open('senti_news/test3.txt', 'r') as news_file2:
    news2 = news_file2.read()


textblob1 = TextBlob(news1)
textblob2 = TextBlob(news2)
textblob3 = TextBlob(text1)



# print out 1st sentence
#print("\nThe whole text:", textblob1)
print("The sentiment index:", textblob1.sentiment)

# print out 2nd sentence
#print("\nThe whole text:", textblob2)
print("The sentiment index:", textblob2.sentiment)


# print out 2nd sentence
#print("\nThe whole text:", textblob3)
print("The sentiment index:", textblob3.sentiment)





