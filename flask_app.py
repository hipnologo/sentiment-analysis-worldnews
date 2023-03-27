import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import pickle
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from flair.models import TextClassifier
from flair.data import Sentence
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zABCxec]i'

@app.route('/', methods=['GET', 'POST'])
def home():
    # session = session
    if request.method == 'POST':
        # Handle form submission
        session['apiKey'] = request.form['apiKey']
        selected_country = request.form['selected_country']
        source_type = request.form['source_type']
        selected_model = request.form.get('selected_model', 'vader')
        selected_features = request.form.getlist('selected_features')
    else:
        # Display the form
        session.clear()  # Initialize the session
        selected_model = 'vader'
        selected_features = []
        return render_template('index.html')

    # Select news country from an array list of country codes
    countries = ['br', 'us', 'gb', 'au', 'ca', 'de', 'fr', 'in', 'it', 'jp', 'mx', 'ru', 'za']
    selected_country = request.form.get('selected_country', 'us')

    try:
        # Import news from around the world using a public API
        world_news_url = 'https://newsapi.org/v2/top-headlines?country='+ selected_country + '&apiKey=' + session.get('apiKey', '')
        world_news = requests.get(world_news_url, verify=False).json()
        # check if the request was successful
        if world_news['status'] == 'ok':
            # convert the response to a DataFrame
            world_news = pd.DataFrame(world_news['articles'])
            # display the first 5 rows of the DataFrame
            world_news.head(50)

            sentiment_title = 'Sentiment Analysis of World News'

    except requests.exceptions.RequestException as e:
        error_msg = f"Error getting world news: {e}"
        return render_template('error.html', error_msg=error_msg)

    if 'world_news' not in locals() and 'world_news' not in globals():
        error_msg = f"World news has not been loaded. Please select 'News' as the source type and try again."
        return render_template('error.html', error_msg=error_msg)

    # Apply a sentiment analysis to the selected news headlines or tweets
    selected_headlines = world_news[['title', 'description', 'author']].copy()
    selected_headlines['title'] = selected_headlines['title'] + ' ' + selected_headlines['description']

    if 'VADER' in selected_model:
        score = SentimentIntensityAnalyzer().polarity_scores(selected_headlines['title'])
    elif 'BERT' in selected_model:
        # Apply sentiment analysis using BERT
        pass
    elif 'RoBERTa' in selected_model:
        # Apply sentiment analysis using RoBERTa
        pass
    elif 'TextBlob' in selected_model:
        # Apply sentiment analysis using TextBlob
        score = TextBlob(selected_headlines['title'][0]).sentiment
    elif 'Flair' in selected_model:
        # Apply sentiment analysis using Flair
        classifier = TextClassifier.load('en-sentiment')
        sentence = Sentence(selected_headlines['title'][0])
        classifier.predict(sentence)
        score = sentence.labels[0].score
        sentiment = sentence.labels[0].value

        # Generate the sentiment analysis score text and color based on the score
        score_text = 'Positive' if sentiment == 'POSITIVE' else 'Negative' if sentiment == 'NEGATIVE' else 'Neutral'
        color = 'green' if sentiment == 'POSITIVE' else 'red' if sentiment == 'NEGATIVE' else 'gray'
        score_value = f"<span style='font-size:32px;color:{color};'>{score}</span>"
        score_text = f"<span style='font-size:24px;color:{color};'>{score_text}</span>"

        # Display the sentiment analysis score and breakdown in the dashboard
        sentiment_title = 'Sentiment Analysis of News from ' + selected_country.upper() + ' (' + world_news['author'].iloc[0] + ')'
        sentiment_score = f"Sentiment Score: <br>{score_value} <br>{score_text}"
        sentiment_breakdown = 'The sentiment score breakdown: ' + str(score)

    # Render the dashboard template with the selected news source headlines and sentiment scores
    return render_template('index.html', 
                        sentiment_title=sentiment_title, 
                        sentiment_score=sentiment_score, 
                        sentiment_breakdown=sentiment_breakdown, 
                        news=selected_headlines.to_html(index=False), 
                        save_message=save_message)

#Run the app
if __name__ == '__main__':
    app.run(debug=True)