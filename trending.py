import os
import tweepy
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Read Twitter API keys from environment variables
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

analyzer = SentimentIntensityAnalyzer()

st.title("Twitter Sentiment Analysis")

trending_hashtag = st.text_input("Enter a hashtag or topic:", value="#your_trending_hashtag")

if st.button("Analyze"):
    tweets = api.search_tweets(q=trending_hashtag, count=100, lang="en", tweet_mode="extended")
    
    if tweets:
        for tweet in tweets:
            full_text = tweet.full_text
            sentiment = analyzer.polarity_scores(full_text)
            st.write(f"Tweet: {full_text}")
            st.write(f"Sentiment: {sentiment}")
            st.write("---")
    else:
        st.write("No tweets found. Please try another hashtag or topic.")
