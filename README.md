# Sentiment Analysis of World News

This script loads news headlines or tweets using APIs, applies sentiment analysis to the headlines or tweets,
and displays the results in a Streamlit dashboard. The sentiment analysis is performed using the VADER sentiment analysis tool.

The dashboard allows the user to select a news source or hashtag, and displays
the sentiment analysis score for the selected news source or hashtag, as well as a table of the news headlines or tweets and their sentiment scores.

This script requires pandas, numpy, matplotlib, seaborn, nltk, pickle, streamlit, requests, json, plotly.express, plotly.graph_objects,
vaderSentiment, and tweepy to be installed.

## Usage

- Clone the repository:
    ```
    git clone https://github.com/username/repo.git
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

## Author

Fabio Carvalho

## Inspired by

Aditya Verma 

## License

This project is licensed under the MIT License. See LICENSE for more information.
