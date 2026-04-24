import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class NewsSentiment:

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, query="ONGC"):

        url = f"https://news.google.com/rss/search?q={query}+share+price+India&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)

        sentiments = []
        headlines = []

        for entry in feed.entries[:10]:
            print(entry.title)   # DEBUG
            title = entry.title

            score = self.analyzer.polarity_scores(title)["compound"]

            sentiments.append(score)
            headlines.append(title)
       
        # avoid division error

        if len(sentiments) == 0:
            avg_sentiment = 0
        else:
            avg_sentiment = sum(sentiments) / len(sentiments)

        return {
            "score": avg_sentiment,
            "headlines": headlines
        }