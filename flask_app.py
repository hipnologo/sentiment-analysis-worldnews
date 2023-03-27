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
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def home():
    #session = session
    if request.method == 'POST':
        # Handle form submission
        session['apiKey'] = request.form['apiKey']
        selected_country = request.form['selected_country']
        source_type = request.form['source_type']
    else:
        # Display the form
        session.clear()  # Initialize the session
        return render_template('index.html')

    # Select news country from an array list of country codes
    countries = ['br', 'us', 'gb', 'au', 'ca', 'de', 'fr', 'in', 'it', 'jp', 'mx', 'ru', 'za']
    selected_country = request.form.get('selected_country', 'us')

    # Add an option to pull tweets instead of world_news
    source_type = request.form.get('source_type', 'News')

    if source_type == 'News':
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

    else:
        if 'world_news' not in locals() and 'world_news' not in globals():
            error_msg = f"World news has not been loaded. Please select 'News' as the source type and try again."
            return render_template('error.html', error_msg=error_msg)

        # Apply a sentiment analysis to the selected news headlines or tweets
        selected_headlines = world_news[['title', 'description', 'author']].copy()
        selected_headlines['title'] = selected_headlines['title'] + ' ' + selected_headlines['description']
        score = SentimentIntensityAnalyzer().polarity_scores(selected_headlines['title'])
        sentiment_title = 'Sentiment Analysis of News from ' + selected_country.upper() + ' (' + world_news['author'].iloc[0] + ')'

        # Generate the sentiment analysis score text and color based on the compound score
        score_text = 'Positive' if score['compound'] >= 0.05 else 'Negative' if score['compound'] <= -0.05 else 'Neutral'
        color = 'green' if score['compound'] >= 0.05 else 'red' if score['compound'] <= -0.05 else 'gray'
        score_value = f"<span style='font-size:32px;color:{color};'>{score['compound']}</span>"
        score_text = f"<span style='font-size:24px;color:{color};'>{score_text}</span>"

        # Display the sentiment analysis score and breakdown in the dashboard
        sentiment_score = f"Sentiment Score: <br>{score_value} <br>{score_text}"
        sentiment_breakdown = 'The sentiment score breakdown: ' + str(score)

        # Save sentiment analysis scores to a pickle file with filename sentiment_analysis_scores + date and time
        if request.form.get('save_scores'):
            dateandtime = datetime.datetime.now().strftime("%Y%m%d") #strftime("%Y%m%d-%H%M%S")
            filename = 'sentiment_analysis_scores_' + dateandtime + '.pkl'
            try:
                with open(filename, 'wb') as f:
                    pickle.dump(score, f)
                save_message = f'Sentiment analysis scores saved successfully to {filename}.'
            except Exception as e:
                save_message = f"Error saving sentiment analysis scores: {e}"

        # Render the dashboard template with the selected news source headlines and sentiment scores
        return render_template('index.html', 
                               sentiment_title=sentiment_title, 
                               sentiment_score=sentiment_score, 
                               sentiment_breakdown=sentiment_breakdown, 
                               news=selected_headlines.to_html(index=False), 
                               save_message=save_message)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
