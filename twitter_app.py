import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import pickle
import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
import os
import ast

st.expander("About this app", expanded=False).write(
"""
This script loads news headlines or tweets using APIs, applies sentiment analysis to the headlines or tweets,
and displays the results in a Streamlit dashboard. The sentiment analysis is performed using the VADER sentiment analysis tool.

The dashboard allows the user to select a news source or hashtag, and displays
the sentiment analysis score for the selected news source or hashtag, as well as a table of the news headlines or tweets and their sentiment scores.

This script requires pandas, numpy, matplotlib, seaborn, nltk, pickle, streamlit, requests, json, plotly.express, plotly.graph_objects,
vaderSentiment, and tweepy to be installed.

Usage:
  - Run the script.
  - Wait for the news or tweets to load from the API.
  - Select a news source or hashtag from the sidebar to filter the headlines or tweets and see the sentiment analysis score for that source or hashtag.
  - The dashboard will display a table of the news headlines or tweets and their sentiment scores.


Author: Fabio Carvalho

Inspired by: Aditya Verma 
"""
)

# Capture apiKey from environment variable or user input and save it in session
apiKey = os.getenv('NEWS_API_KEY')
if apiKey is None:
    apiKey = st.session_state.get('apiKey')
    if not apiKey:
        apiKey = st.text_input('Enter API Key:')
        st.session_state['apiKey'] = apiKey

# Select news country from an array list of country codes
countries = ['br', 'us', 'gb', 'au', 'ca', 'de', 'fr', 'in', 'it', 'jp', 'mx', 'ru', 'za']
selected_country = st.sidebar.selectbox('Country', ('us', *countries))

st.sidebar.subheader('Select the news source or hashtag')

# Add an option to pull tweets instead of world_news
source_type = st.sidebar.selectbox('Source Type', ('News', 'Tweets'))
if source_type == 'News':
    try:
        # Import news from around the world using a public API
        world_news_url = 'https://newsapi.org/v2/top-headlines?country='+ selected_country + '&apiKey=' + apiKey
        world_news = requests.get(world_news_url, verify=False).json()
        # check if the request was successful
        if world_news['status'] == 'ok':
            # convert the response to a DataFrame
            world_news = pd.DataFrame(world_news['articles'])
            # display the first 5 rows of the DataFrame
            world_news.head(50)

            st.title('Sentiment Analysis of World News')
        else:
            st.error("Error getting world news. Please check your API key and try again.")
            st.stop()
    except requests.exceptions.RequestException as e:
        st.write(f"Error getting world news: {e}")
else:
    # Get hashtag input from user
    use_hashtag = st.sidebar.checkbox('Use Hashtag Input')
    
    try:
    
        # Capture Twitter API keys from environment variables or user input and save them in session
        apiTwitterKey = os.getenv('API_TWITTER_KEY')
        if apiTwitterKey is None:
            apiTwitterKey = st.session_state.get('apiTwitterKey')
            if not apiTwitterKey:
                apiTwitterKey = st.text_input('Enter API Twitter Key:')
                st.session_state['apiTwitterKey'] = apiTwitterKey
                
        apiKeySecret = os.getenv('API_KEY_SECRET')
        if apiKeySecret is None:
            apiKeySecret = st.session_state.get('apiKeySecret')
            if not apiKeySecret:
                apiKeySecret = st.text_input('Enter API Key Secret:')
                st.session_state['apiKeySecret'] = apiKeySecret

        accessToken = os.getenv('ACCESS_TOKEN')
        if accessToken is None:
            accessToken = st.session_state.get('accessToken')
            if not accessToken:
                accessToken = st.text_input('Enter Access Token:')
                st.session_state['accessToken'] = accessToken

        accessTokenSecret = os.getenv('ACCESS_TOKEN_SECRET')
        if accessTokenSecret is None:
            accessTokenSecret = st.session_state.get('accessTokenSecret')
            if not accessTokenSecret:
                accessTokenSecret = st.text_input('Enter Access Token Secret:')
                st.session_state['accessTokenSecret'] = accessTokenSecret

            
        # Authenticate with Twitter API
        auth = tweepy.OAuth1UserHandler(
            apiTwitterKey, apiKeySecret, accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        if use_hashtag:
            hashtag = st.sidebar.text_input('Hashtag')
            # Set default value for total items
            total_items = st.sidebar.slider('Select the # of Tweets:', 1, 1000, 50)
            #tweets = tweepy.Cursor(api.search_tweets, q=hashtag + ' -filter:retweets', tweet_mode='extended', lang='en', result_type='recent').items(50)
            # Search tweets using Tweepy
            tweets = tweepy.Cursor(api.search_tweets, q=hashtag + ' -filter:retweets', tweet_mode='extended',
                                lang='en', result_type='recent').items(total_items)

            #tweets_df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['text'])
            # Extract tweet attributes and create DataFrame
            tweets_data = []
            for tweet in tweets:
                tweet_dict = {}
                tweet_dict['text'] = tweet.full_text
                tweet_dict['created_at'] = tweet.created_at
                tweet_dict['user_location'] = tweet.user.location
                # Add more tweet attributes as needed
                tweets_data.append(tweet_dict)

            tweets_df = pd.DataFrame(tweets_data)
            
            if tweets_df.empty:
                st.warning("No tweets found. Please try again with different hashtag.")
            else:
                # display the first 5 rows of the DataFrame
                st.title('Sentiment Analysis of Tweets with Hashtag: ' + hashtag)
                selected_tweets = tweets_df.copy()

        else:
            keywords = st.sidebar.text_input('Keywords (comma-separated)')
            if keywords:
                keyword_list = keywords.split(',')
                # Set default value for total items
                total_items = st.sidebar.slider('Select the # of Tweets:', 1, 1000, 50)
                # Get tweets with the specified keywords
                #tweets = tweepy.Cursor(api.search_tweets, q=' OR '.join(keyword_list) + ' -filter:retweets', tweet_mode='extended', lang='en', result_type='recent').items(50)
                tweets = tweepy.Cursor(api.search_tweets, q=' OR '.join(keyword_list) + ' -filter:retweets', tweet_mode='extended',
                                    lang='en', result_type='recent').items(total_items)
                # convert the tweets to a DataFrame
                #tweets_df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['text'])
                
                # Extract tweet attributes and create DataFrame
                tweets_data = []
                for tweet in tweets:
                    tweet_dict = {}
                    tweet_dict['text'] = tweet.full_text
                    tweet_dict['created_at'] = tweet.created_at
                    tweet_dict['user_location'] = tweet.user.location
                    # Add more tweet attributes as needed
                    tweets_data.append(tweet_dict)

                tweets_df = pd.DataFrame(tweets_data)
                
                #tweet_dict['created_at'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                
                if tweets_df.empty:
                    st.warning("No tweets found. Please try again with different keywords.")
                else:
                    # display the first 5 rows of the DataFrame
                    st.title('Sentiment Analysis of Tweets with Keywords: ' + ', '.join(keyword_list))
                    selected_tweets = tweets_df.copy()
            else:
                st.sidebar.warning("Please enter one or more keywords.")

    except requests.exceptions.RequestException as e:
        st.write(f"Error getting tweets: {e}")

# Display the dashboard title
st.markdown('This application is a dashboard to analyze the sentiment of news headlines or tweets.')

if source_type == 'News':
    # Select news source and author from the world_news DataFrame
    news_author = world_news['author'].unique()
    #news_source = world_news['source'].apply(lambda x: ast.literal_eval(x)['name']).unique()
    news_source = world_news['source'].apply(lambda x: x['name']).unique()

    selected_news_source = st.sidebar.selectbox('News Source', ['All'] + list(news_source))
    selected_news_author = st.sidebar.selectbox('News Author', ['All'] + list(news_author))

    # update the DataFrame based on the news source and author selected
    if selected_news_source != 'All' and selected_news_author != 'All':
        selected_world_news = world_news[(world_news['source'] == selected_news_source) & (world_news['author'] == selected_news_author)]
    elif selected_news_source != 'All':
        selected_world_news = world_news[world_news['source'] == selected_news_source]
    elif selected_news_author != 'All':
        selected_world_news = world_news[world_news['author'] == selected_news_author]
    else:
        selected_world_news = world_news

    # Apply a sentiment analysis to the news headlines
    score = SentimentIntensityAnalyzer().polarity_scores(' '.join(selected_world_news['title'].tolist()))
    st.sidebar.subheader('Sentiment Analysis News')

    score_text = 'Positive' if score['compound'] >= 0.05 else 'Negative' if score['compound'] <= -0.05 else 'Neutral'
    color = 'green' if score['compound'] >= 0.05 else 'red' if score['compound'] <= -0.05 else 'gray'
    score_value = f"<span style='font-size:32px;color:{color};'>{score['compound']}</span>"
    score_text = f"<span style='font-size:24px;color:{color};'>{score_text}</span>"
    st.sidebar.markdown(f"Sentiment Score: <br>{score_value} <br>{score_text}", unsafe_allow_html=True)

    st.sidebar.write('The sentiment score breakdown: ', score)
    st.sidebar.write('---')

    # Show the news headlines and sentiment scores in a table
    st.table(selected_world_news[['title', 'description', 'source', 'author']])

else:
    # check if selected_tweets is defined
    if 'selected_tweets' in locals():
        
        # Select the tweets display
        selected_tweets['title'] = selected_tweets['text']
                
        # Apply a sentiment analysis to the tweets
        score = SentimentIntensityAnalyzer().polarity_scores(selected_tweets['text'])
        st.sidebar.write('---')
        st.sidebar.subheader('Sentiment Analysis Tweets')
        
        #st.sidebar.markdown('**Positive**' if score['compound'] >= 0.05 else '**Negative**' if score['compound'] <= -0.05 else '**Neutral**')
        score_text = 'Positive' if score['compound'] >= 0.05 else 'Negative' if score['compound'] <= -0.05 else 'Neutral'
        color = 'green' if score['compound'] >= 0.05 else 'red' if score['compound'] <= -0.05 else 'gray'
        score_value = f"<span style='font-size:32px;color:{color};'>{score['compound']}</span>"
        score_text = f"<span style='font-size:24px;color:{color};'>{score_text}</span>"
        st.sidebar.markdown(f"Sentiment Score: <br>{score_value} <br>{score_text}", unsafe_allow_html=True)

        st.sidebar.write('The sentiment score breakdown: ', score)
        st.sidebar.write('---')
        #st.sidebar.write('The sentiment analysis is: ', end='')
        #st.sidebar.metric(label="Sentiment Score", value=score['compound'])
        
        # Show the tweets and sentiment scores in a table
        #st.table(selected_tweets[['text']])
        st.table(selected_tweets[['text', 'created_at', 'user_location']])

    else:
        st.warning("Please select a keyword to search for tweets.")

if st.sidebar.button('Save sentiment analysis scores'):
    # Save sentiment analysis scores to a pickle file with filename sentiment_analysis_scores + date and time
    dateandtime = datetime.datetime.now().strftime("%Y%m%d")  # strftime("%Y%m%d-%H%M%S")
    filename = 'sentiment_analysis_scores_' + dateandtime + '.pkl'
    
    # Save "created_at" and "user_location" attributes in a CSV file
    csv_filename = 'sentiment_analysis_tweets_' + dateandtime + '.csv'
    
    try:
        with open(filename, 'wb') as f:
            pickle.dump(score, f)
        st.write(f'Sentiment analysis scores saved successfully to {filename}.')
        
        # Save selected_tweets with "created_at" and "user_location" attributes in a CSV file
        selected_tweets[['created_at', 'user_location']].to_csv(csv_filename, index=False)
        st.write(f'Tweets data saved successfully to {csv_filename}.')
    except Exception as e:
        st.error(f"Error saving data: {e}")

