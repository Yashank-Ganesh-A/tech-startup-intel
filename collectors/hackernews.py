import requests
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.db import get_col
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

QUERIES = ["startup", "artificial intelligence", "machine learning", "tech", "programming"]

def collect():
    col = get_col("hackernews")
    col.drop()
    saved = 0

    print("[COLLECTING] HackerNews Stories via Algolia API...")

    for query in QUERIES:
        url = f"https://hn.algolia.com/api/v1/search?tags=story&query={query.replace(' ', '+')}&hitsPerPage=20"
        try:
            res = requests.get(url, headers=HEADERS, timeout=20)
            data = res.json()
            hits = data.get("hits", [])
            print(f"  Query [{query:25}] >> Found {len(hits)} stories")

            for hit in hits:
                try:
                    doc = {
                        "source": "news.ycombinator.com",
                        "title": hit.get("title", "N/A"),
                        "author": hit.get("author", "N/A"),
                        "points": hit.get("points", 0) or 0,
                        "comments": hit.get("num_comments", 0) or 0,
                        "url": hit.get("url", "N/A"),
                        "story_id": hit.get("objectID", "N/A"),
                        "query_tag": query,
                        "created_at": hit.get("created_at", "N/A"),
                        "scraped_at": datetime.now()
                    }
                    col.insert_one(doc)
                    saved += 1
                except:
                    continue

        except Exception as e:
            print(f"  Error for query {query}: {e}")
            continue

    print(f"  Total saved: {saved} HackerNews stories\n")
    return saved

if __name__ == "__main__":
    collect()