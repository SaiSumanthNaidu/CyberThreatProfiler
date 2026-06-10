import feedparser

RSS_FEEDS = [

    "https://feeds.feedburner.com/TheHackersNews",

    "https://www.bleepingcomputer.com/feed/",

    "https://www.cisa.gov/news.xml"

]


def fetch_articles():

    articles = []

    for url in RSS_FEEDS:

        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:

            articles.append({

                "title": entry.title,

                "description": getattr(
                    entry,
                    "summary",
                    ""
                )

            })

    return articles