# Sentiment Analysis of World News

This is a Python script that loads news headlines from around the world using the News API, applies sentiment analysis to the headlines, and displays the results in a Streamlit dashboard. The sentiment analysis is performed using the VADER sentiment analysis tool.

![GitHub](https://img.shields.io/github/license/hipnologo/sentiment-analysis-worldnews)

## Requirements
- pandas
- numpy
- matplotlib
- seaborn
- nltk
- pickle
- streamlit
- requests
- json
- plotly.express
- plotly.graph_objects
- vaderSentiment

## Usage
1. Clone the repository:
``git clone https://github.com/username/repo.git``

1. Install the required packages:
`pip install -r requirements.txt`

1. Run the script:
`streamlit run sentiment_analysis.py`

1. Wait for the news to load from the News API.

2. Select a news source from the sidebar to filter the headlines and see the sentiment analysis score for that source.

3. The dashboard will display a table of the news headlines and their sentiment scores.
