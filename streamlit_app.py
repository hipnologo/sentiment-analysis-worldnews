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
import os
import ast

st.expander("About this app", expanded=False).write(
"""
This script loads news headlines or tweets using APIs, applies sentiment analysis to the headlines or tweets,
and displays the results in a Streamlit dashboard. The sentiment analysis is performed using the VADER sentiment analysis tool.

The dashboard allows the user to select a news source for a sentiment analysis score relative to the selected news source, 
as well as a table of the news headlines their sentiment scores.

This script requires at least pandas, numpy, nltk, pickle, streamlit, requests, json, os, and vaderSentiment to be installed.

Usage:
  - Run the script.
  - Wait for the news or tweets to load from the API.
  - Select a news source from the sidebar to filter the headlines and see the sentiment analysis score for that source.
  - The dashboard will display a table of the news headlines and their sentiment scores.

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

# Display the dashboard title
st.markdown('This application is a dashboard to analyze the sentiment of news headlines.')


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
    #selected_world_news = world_news[world_news['source'] == selected_news_source]
    selected_world_news = world_news[world_news['source'].apply(lambda x: x['name']) == selected_news_source]
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
        #selected_tweets[['created_at', 'user_location']].to_csv(csv_filename, index=False)
        #st.write(f'Tweets data saved successfully to {csv_filename}.')
    except Exception as e:
        st.error(f"Error saving data: {e}")

