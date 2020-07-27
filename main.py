import string
from collections import Counter
from datetime import date

import matplotlib.pyplot as plt

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import GetOldTweets3 as got

def get_tweets(x):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(x)\
                                           .setSince("2020-01-01")\
                                           .setUntil("2020-07-26")\
                                           .setMaxTweets(200)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    text_tweets=[[tweet.text] for tweet in tweets]
    return(text_tweets)

def count_emotions(txtfile, words):
    emotion_list=[]
    file=open(txtfile,'r')
    for line in file:
        clean_line=line.replace('\n','').replace(',','').replace("'",'').strip()
        word,emotion=clean_line.split(':')
        
        if word in words:
            emotion_list.append(emotion)
    
    x=Counter(emotion_list)        
    return(x)

def sentiment_analyze(sentiment_text):
    score=SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    neg=score['neg']
    pos=score['pos']
    if(neg>pos):
        print("The message has a Negative Sentiment")
    elif(pos>neg):
        print("the message has a Positive Sentiment")
    elif(neg==pos):
        print("The message has a Neutral Sentiment")

def plotgraph(x):
    plt.bar(x.keys(),x.values())
    plt.savefig('emotion_graph.png')
    plt.show()

topic=input("enter topic you want to search tweets for:")
text=""
text_tweets=get_tweets(topic)
length=len(text_tweets)
for i in range(length):
    text=text_tweets[i][0]+ " "+ text

text=text.lower()

#create a table to replace/translate characters as per mapping table
cleaned_text=text.translate(str.maketrans('','',string.punctuation))

#tokenizing the text
word_list=word_tokenize(cleaned_text,'english')

#removing all the stop words(words that dont add emotion to the sentence)
for word in word_list:
    if word in stopwords.words("english"):
        word_list.remove(word) 

#counting different emotions in cleaned word_list
emotion_list=count_emotions("emotions.txt",word_list)
plotgraph(emotion_list)
sentiment_analyze(cleaned_text)


