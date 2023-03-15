import os
import tweepy as tw
from tweepy import Stream
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class StreamListener(tw.Stream):
    def __init__(self, streamlit_text_output):
        super().__init__()
        self.analyzer = SentimentIntensityAnalyzer()
        self.streamlit_text_output = streamlit_text_output

    def on_status(self, status):
        full_text = status.text
        sentiment = self.analyzer.polarity_scores(full_text)
        self.streamlit_text_output.write(f"Tweet: {full_text}\nSentiment: {sentiment}\n")

# Read Twitter API keys from environment variables
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)

st.title("Real-time Twitter Sentiment Analysis")

keyword = st.text_input("Enter a keyword to track:", value="example")

stop_button = st.empty()

if st.button("Start Tracking"):
    with st.empty() as text_output:
        stream_listener = StreamListener(text_output)
        stream = tw.Stream(auth=auth, listener=stream_listener)

        stop_button.text("Tracking tweets. Click to stop.")

        while not stop_button.button("Stop Tracking"):
            try:
                stream.filter(track=[keyword], is_async=True)
                st.sleep(1)
            except Exception as e:
                text_output.write(f"Error: {e}")
                break

        stream.disconnect()
        stop_button.empty()