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
```bash
git clone https://github.com/username/repo.git
cd repo```

2. Install the required packages:
```pip install -r requirements.txt```

3. Run the script:
```streamlit run sentiment_analysis.py```

4. Wait for the news to load from the News API.

5. Select a news source from the sidebar to filter the headlines and see the sentiment analysis score for that source.

6. The dashboard will display a table of the news headlines and their sentiment scores.
