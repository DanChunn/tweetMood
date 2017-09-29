import tweepy
from textblob import TextBlob
import csv
import re

# Step 1 - Authenticate
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'

access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Step 2 - Prepare search
hash_tag = '#divinityoriginalsin2'
since_date = "2017-09-20"
until_date = "2017-09-29"
number_of_tweets = 100

public_tweets = api.search(hash_tag, count = number_of_tweets, since = since_date, until = until_date)

# Step 3 - write to CSV
def clean_tweet(tweet):

	#https://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression/8377440
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
    	return 'negative'

with open('%s_tweets.csv' % hash_tag, 'w', encoding='utf8') as csvfile:
	writer = csv.writer(csvfile, delimiter=",")
	for tweet in public_tweets:
		c_tweet = clean_tweet(tweet.text)
		sentiment = get_tweet_sentiment(c_tweet)
		arr = [c_tweet, sentiment]
		writer.writerow(arr)