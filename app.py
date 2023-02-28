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


# Import news from around the world using a public API
world_news_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=4d1c65d85f4347e4913e2ed023cf0bf2'
world_news = requests.get(world_news_url, verify=False).json()
# check if the request was successful
if world_news['status'] == 'ok':
    # convert the response to a DataFrame
    world_news = pd.DataFrame(world_news['articles'])
    # display the first 5 rows of the DataFrame
    world_news.head(50)

st.title('Sentiment Analysis of World News')
st.markdown('This application is a dashboard to analyze the sentiment of news headlines.')

st.sidebar.title('Options')
st.sidebar.write('---')
st.sidebar.subheader('Select the news source')

# Select news source from the world_news DataFrame author column
news_author = world_news['author'].unique()
selected_news_author = st.sidebar.selectbox('News Source', ('All', *news_author))

# update the DataFrame based on the news source selected
selected_world_news = world_news[world_news['author'] == selected_news_author] if selected_news_author != 'All' else world_news



# Apply a sentiment analysis to the news headlines
score = SentimentIntensityAnalyzer().polarity_scores(selected_world_news['title'])
st.sidebar.write('---')
st.sidebar.subheader('Sentiment Analysis Score')
st.sidebar.write('The sentiment score is: ', score)
st.sidebar.write('---')
st.sidebar.write('The sentiment analysis is: ', end='')
st.sidebar.metric(label="Sentiment Score", value=score['compound'])
st.sidebar.write('Positive' if score['compound'] >= 0.05 else 'Negative' if score['compound'] <= -0.05 else 'Neutral')

# Show the news headlines and sentiment scores in a table
st.table(selected_world_news[['title', 'description', 'author']])
