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

st.title("Brand vs. Competitor Sentiment Analysis")

brand_name = st.text_input("Enter your brand name:", value="your_brand_name")
competitor_name = st.text_input("Enter your competitor's name:", value="your_competitor_name")

brands = [brand_name, competitor_name]

if st.button("Analyze"):
    for brand in brands:
        tweets = api.search(q=brand, count=100, lang="en", tweet_mode="extended")
        total_sentiment = 0

        for tweet in tweets:
            full_text = tweet.full_text
            sentiment = analyzer.polarity_scores(full_text)
            total_sentiment += sentiment['compound']

        avg_sentiment = total_sentiment / len(tweets)
        st.write(f"Average sentiment for {brand}: {avg_sentiment}")
