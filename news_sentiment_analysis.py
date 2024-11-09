import requests
from textblob import TextBlob
import streamlit as st

# Your actual News API key
NEWS_API_KEY = 'dd60e8afc6fe45cebc3cf3fc3f893a06'

# Function to fetch news articles based on a keyword
def fetch_news(keyword):
    url = f'https://newsapi.org/v2/everything?q={keyword}&language=en&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    articles = response.json().get("articles", [])
    news_data = []
    
    for article in articles:
        title = article["title"]
        description = article["description"] or ""
        content = title + " " + description
        sentiment = TextBlob(content).sentiment.polarity
        sentiment_category = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        news_data.append({"title": title, "sentiment": sentiment_category})
    
    return news_data

# Streamlit Dashboard
st.title("Real-Time Sentiment Analysis on News Articles")
st.write("Enter a keyword to fetch news articles and analyze sentiment in real-time.")

keyword = st.text_input("Keyword", "Technology")
if st.button("Fetch News"):
    with st.spinner("Fetching news articles..."):
        articles = fetch_news(keyword)
        st.success(f"Fetched {len(articles)} articles for '{keyword}'")

    # Count sentiment categories
    positive, negative, neutral = 0, 0, 0
    for article in articles:
        if article['sentiment'] == 'Positive':
            positive += 1
        elif article['sentiment'] == 'Negative':
            negative += 1
        else:
            neutral += 1

    # Display results
    st.write(f"**Positive**: {positive}, **Negative**: {negative}, **Neutral**: {neutral}")

    st.subheader("Sample Articles")
    for article in articles[:10]:  # Display the first 10 articles
        st.write(f"{article['title']} - Sentiment: {article['sentiment']}")
