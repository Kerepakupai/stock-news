import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "STOCK_API_KEY"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "NEWS_API_KEY"

TWILIO_ACCOUNT_SID = "TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "TWILIO_PHONE_NUMBER"

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# Get yesterday's closing stock price.
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value["4. close"] for (_, value) in data.items()]
yesterday_closing_price = float(data_list[0])

# Get the day before yesterday's closing stock price
day_before_yesterday_closing_price = float(data_list[1])

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
diff_price = abs(yesterday_closing_price - day_before_yesterday_closing_price)

up_down = None
if yesterday_closing_price > day_before_yesterday_closing_price:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday
# and closing price the day before yesterday.
diff_percent = (diff_price / yesterday_closing_price) * 100

# Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
# If TODO4 percentage is greater than 5 then print("Get News").
if diff_percent > 5:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "language": "en",
        "sortBy": "relevance",
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response.json()["articles"]

    # Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [
        f"{COMPANY_NAME}:{up_down}{round(diff_percent)}% \nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in articles
    ]

    # Send each article as a separate message via Twilio.
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_PHONE_NUMBER,
            to='+56951149245'
        )
