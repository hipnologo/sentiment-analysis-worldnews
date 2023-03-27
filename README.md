# Sentiment Analysis of World News

This script loads news headlines or tweets using APIs, applies sentiment analysis to the headlines or tweets, and displays the results in a Streamlit dashboard. The sentiment analysis is performed using the VADER sentiment analysis tool.

The dashboard allows the user to select a news source or hashtag, and displays the sentiment analysis score for the selected news source or hashtag, as well as a table of the news headlines or tweets and their sentiment scores.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Forks](https://img.shields.io/github/forks/hipnologo/sentiment-analysis-worldnews)](https://github.com/hipnologo/sentiment-analysis-worldnews/network/members)
[![Stars](https://img.shields.io/github/stars/hipnologo/sentiment-analysis-worldnews)](https://github.com/hipnologo/sentiment-analysis-worldnews/stargazers)
[![Issues](https://img.shields.io/github/issues/hipnologo/sentiment-analysis-worldnews)](https://github.com/hipnologo/sentiment-analysis-worldnews/issues)
## Usage

- Clone the repository:
    ```
    git clone https://github.com/hipnologo/sentiment-analysis-worldnews.git
    ```

- Install the required packages:
    ```
    pip install -r requirements.txt
    ```

- Run the script:
    ```
    streamlit run app.py
    ```

- Wait for the news or tweets to load from the API.

- Select a news source or hashtag from the sidebar to filter the headlines or tweets and see the sentiment analysis score for that source or hashtag.

- The dashboard will display a table of the news headlines or tweets and their sentiment scores.

## vaderSentiment Library

`vaderSentiment` is a Python library that provides sentiment analysis capabilities, specifically designed for working with social media text. VADER stands for Valence Aware Dictionary and sEntiment Reasoner. It is a rule-based sentiment analysis tool that is particularly good at understanding the sentiment in short pieces of text, like tweets or comments, and can handle slang, emojis, and unconventional grammar.

The line of code you provided is an import statement in Python:

```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
```

This line imports the SentimentIntensityAnalyzer class from the `vaderSentiment.vaderSentiment` module. The `SentimentIntensityAnalyzer` class is the main component of the library and is used to analyze the sentiment of a given text.

To use VADER for sentiment analysis, you can follow these steps:

1. Install the vaderSentiment library, if you haven't already, using pip:
```pip install vaderSentiment```

2. Import the SentimentIntensityAnalyzer class in your Python script:
```from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer```

3. Create an instance of the SentimentIntensityAnalyzer class:
```analyzer = SentimentIntensityAnalyzer()```

4. Analyze the sentiment of a text:
```
text = "I love this product!"
sentiment = analyzer.polarity_scores(text)
```

5. Interpret the results:
The polarity_scores() method returns a dictionary containing the following keys:
```
'neg': Negative sentiment score (0 to 1)
'neu': Neutral sentiment score (0 to 1)
'pos': Positive sentiment score (0 to 1)
'compound': Compound sentiment score (-1 to 1)
```
The compound score can be used to classify the overall sentiment as positive, negative, or neutral. Typically, a threshold is applied, such as:

* **Positive** sentiment: compound score > 0.05
* **Neutral** sentiment: -0.05 <= compound score <= 0.05
* **Negative** sentiment: compound score < -0.05
Keep in mind that these threshold values can be adjusted according to the specific context or requirements of your project.

Using the `vaderSentiment` library in conjunction with `tweepy` allows you to perform sentiment analysis on tweets fetched from Twitter. Tweepy is a popular Python library for accessing the Twitter API, making it easy to collect tweets for analysis. By combining these two libraries, you can analyze the sentiment of tweets and gain valuable insights into public opinions or trends.

### Some possibilities 

Examples of use for sentiment analysis using `vaderSentiment` and `tweepy`:

1. **Real-time sentiment analysis**: Monitor and analyze the sentiment of tweets in real-time as they are posted. This can be useful for tracking public reactions to events, product launches, or news.

2. **Brand monitoring**: Keep track of how people are talking about your brand, products, or services on Twitter. By analyzing sentiment, you can gauge customer satisfaction and identify areas that may need improvement.

3. **Competitor analysis**: Compare the sentiment of tweets about your brand with those of your competitors. This can help you understand your brand's position in the market and identify potential opportunities or threats.

4. **Trending topics**: Analyze the sentiment of tweets related to trending topics or hashtags. This can help you understand public sentiment about a particular subject or event.

5. **Influencer analysis**: Identify influential users in your domain by analyzing the sentiment of their tweets and how they are received by their audience. This can help you find potential influencers for your brand or partnerships.

6. **Public opinion on political and social issues**: Analyze the sentiment of tweets related to political candidates, parties, or social issues to gauge public opinion and identify trends in public discourse.


## Contributing

Contributions are always welcome! If you have any suggestions or would like to add features, please open an issue or create a pull request.

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

## License

This project is licensed under the MIT License. See LICENSE for more information.
