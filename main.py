from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'AMD', 'FB']

news_tables = {}
for ticker in tickers:
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'sentiment-stock'})
    response = urlopen(req)

    html = BeautifulSoup(response, 'html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    break

# amzn_data = news_tables['AMZN']
# amzn_rows = amzn_data.findAll('tr')
#
# for index, row in enumerate(amzn_rows):
#     if row.a is not None:
#         title = row.a.text
#         timestamp = row.td.text
#         print(timestamp + " " + title)
#     else:
#         continue

parsed_data = []

for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        if row.a is not None:
            title = row.a.text
            date_data = row.td.text.strip().split(" ")  # counts how many split values there are
            if len(date_data) == 1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]
        else:
            continue
        parsed_data.append([ticker, date, time, title])
print(parsed_data)