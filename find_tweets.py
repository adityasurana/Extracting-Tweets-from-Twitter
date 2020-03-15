from tweepy import OAuthHandler
from tweepy import API
import tweepy
import pandas as pd
import sys
import os

#Twitter API credentials
consumer_key = "Enter your consumer key"
consumer_secret = "Enter your consumer secret"
access_token = "Enter your access token"
access_token_secret = "Enter your access token secret"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

tweet_id=[]
tweet_time=[]
tweet_text=[]
retweet_count=[]
like_count=[]

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets 

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    #print(new_tweets.id_str)
    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        #print("getting tweets before tweet id %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #print("...%s tweets downloaded so far" % (len(alltweets)))    
    
    
    for tweet in alltweets:
        #print(tweet.id_str)
        tweet_id.append(str(tweet.id_str))
        tweet_time.append(tweet.created_at)
        tweet_text.append(tweet.text.encode("utf-8"))
        try:
            tweets = api.get_status(int(tweet.id_str))
            retweet_count.append(tweets.retweet_count)
            like_count.append(tweets.favorite_count)
        
        except:
            #print("coming here")
            retweet_count.append(0)
            like_count.append(0)

screen_name = input("Enter the screen name of the person whoose tweets is to be extracted")
get_all_tweets(screen_name)

        
df = pd.DataFrame(list(zip(tweet_id, tweet_time, tweet_text, retweet_count, like_count)),
                  columns = ['Tweet Id', 'Tweet Time', 'Tweet Text', 'Retweet Count', 'Like Count'])
outputfile_path = "%s\\user_tweets.xlsx" %dir_path
df.to_excel(outputfile_path, index=False)


    
