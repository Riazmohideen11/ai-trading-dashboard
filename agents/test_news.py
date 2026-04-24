import feedparser

url = f"https://news.google.com/rss/search?q={query}+share+price+India&hl=en-IN&gl=IN&ceid=IN:en"
feed = feedparser.parse(url)

for entry in feed.entries[:5]:
    print(entry.title)