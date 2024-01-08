from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'GOOG', 'META', 'TSLA']

news_tables = {}
for ticker in tickers:
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'sentiment-stock'})
    response = urlopen(req)

    html = BeautifulSoup(response, 'html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table


parsed_data = []

for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        if row.a is not None:
            title = row.a.text
            date_data = row.td.text.strip().split(" ")  # counts how many split values there are
            if len(date_data) == 1:
                time = date_data[0]
            else:
                if date_data[0] == 'Today':
                    parsed_date = date.today()
                    time = date_data[1]
                else:
                    parsed_date = date_data[0]
                    time = date_data[1]
        else:
            continue
        parsed_data.append([ticker, parsed_date, time, title])

df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
vader = SentimentIntensityAnalyzer()

f = lambda title: vader.polarity_scores(title)['compound'] # takes in any string (title in this fn) and just gives back the compound score
df['compound'] = df['title'].apply(f) # creates new column in df
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

mean_df = df.groupby(['ticker', 'date'])['compound'].mean().unstack(level=0)
mean_df.plot(kind='bar')

plt.show()
