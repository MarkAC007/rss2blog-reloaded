# rss_parser.py

import feedparser

from datetime import datetime, timedelta

def parse_rss_feed(file_path):
    rss_feed_list = []
    with open(file_path, "r") as file:
        for line in file:
            feed = feedparser.parse(line.strip())
            for entry in feed.entries:
                # Check if the entry was published today
                if datetime(*entry.published_parsed[:6]) >= datetime.now() - timedelta(days=1):
                    rss_feed_list.append({
                        "title": entry.title,
                        "description": entry.description,
                        "url": entry.link  # Added this line
                    })
    return rss_feed_list

