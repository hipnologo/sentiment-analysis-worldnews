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
import tweepy

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Capture apiKey from user input and save it in session
        apiKey = request.form.get('apiKey')
        session['apiKey'] = apiKey

    # Select news country from an array list of country codes
    countries = ['br', 'us', 'gb', 'au', 'ca', 'de', 'fr', 'in', 'it', 'jp', 'mx', 'ru', 'za']
    selected_country = request.form.get('selected_country') or 'us'

    # Add an option to pull tweets instead of world_news
    source_type = request.form.get('source_type') or 'News'

    if source_type == 'News':
        try:
            # Import news from around the world using a public API
            world_news_url = 'https://newsapi.org/v2/top-headlines?country='+ selected_country + '&apiKey=' + session['apiKey']
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
        # Get hashtag input from user
        use_hashtag = request.form.get('use_hashtag')
        selected_tweets = None

        try:
            #st.title('Sentiment Analysis of Tweets with Keywords: ' + ', '.join(keyword_list))
            #selected_tweets = tweets_df.copy()

            # Capture Twitter API keys from user input and save them in session
            apiTwitterKey = request.form.get('apiTwitterKey')
            session['apiTwitterKey'] = apiTwitterKey

            apiKeySecret = request.form.get('apiKeySecret')
            session['apiKeySecret'] = apiKeySecret

            accessToken = request.form.get('accessToken')
            session['accessToken'] = accessToken

            accessTokenSecret = request.form.get('accessTokenSecret')
            session['accessTokenSecret'] = accessTokenSecret

            # Authenticate with Twitter API
            auth = tweepy.OAuth1UserHandler(
                apiTwitterKey, apiKeySecret, accessToken, accessTokenSecret)
            api = tweepy.API(auth)

            if use_hashtag:
                hashtag = request.form.get('hashtag')
                tweets = tweepy.Cursor(api.search_tweets, q=hashtag + ' -filter:retweets', tweet_mode='extended', lang='en', result_type='recent').items(50)
                tweets_df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['text'])
                if tweets_df.empty:
                    warning_msg = "No tweets found. Please try again with different hashtag."
                    return render_template('warning.html', warning_msg=warning_msg)
                else:
                    # display the first 5 rows of the DataFrame
                    sentiment_title = f'Sentiment Analysis of Tweets with Hashtag: {hashtag}'
                    selected_tweets = tweets_df.copy()
            else:
                keywords = request.form.get('keywords')
                if keywords:
                    keyword_list = keywords.split(',')
                    # Get tweets with the specified keywords
                    tweets = tweepy.Cursor(api.search_tweets, q=' OR '.join(keyword_list) + ' -filter:retweets', tweet_mode='extended', lang='en', result_type='recent').items(50)
                    # convert the tweets to a DataFrame
                    tweets_df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['text'])
                    if tweets_df.empty:
                        warning_message = "No tweets found. Please try again with different keywords."
                        return render_template('index.html', warning_message=warning_message)
                    else:
                        # display the first 5 rows of the DataFrame
                        sentiment_title = f'Sentiment Analysis of Tweets with Keywords: {", ".join(keyword_list)}'
                        selected_tweets = tweets_df.copy()
                else:
                    warning_message = "Please enter one or more keywords."
                    return render_template('index.html', warning_message=warning_message)

        except requests.exceptions.RequestException as e:
            error_message = f"Error getting tweets: {e}"
            return render_template('index.html', error_message=error_message)

        # Apply a sentiment analysis to the selected news headlines or tweets
        if source_type == 'News':
            selected_headlines = selected_world_news[['title', 'description', 'author']].copy()
            selected_headlines['title'] = selected_headlines['title'] + ' ' + selected_headlines['description']
            score = SentimentIntensityAnalyzer().polarity_scores(selected_headlines['title'])
            sentiment_title = 'Sentiment Analysis of News from ' + selected_country.upper() + ' (' + selected_news_author + ')'
        else:
            selected_headlines = selected_tweets[['text']].copy()
            score = SentimentIntensityAnalyzer().polarity_scores(selected_tweets['text'])

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
    # Render the initial dashboard template with the apiKey form
    return render_template('index.html', apiKey=session.get('apiKey'), countries=countries, selected_country=selected_country, source_type=source_type)

if __name__ == '__main__':
    app.run(debug=True)