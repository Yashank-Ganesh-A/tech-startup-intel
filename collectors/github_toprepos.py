import requests
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.db import get_col
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/vnd.github.v3+json"
}

TOPICS = ["machine-learning", "web-development", "data-science", "devops", "cybersecurity"]

def collect():
    col = get_col("github_toprepos")
    col.drop()
    saved = 0

    print("[COLLECTING] GitHub Top Repositories via API...")

    for topic in TOPICS:
        url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page=20"
        try:
            res = requests.get(url, headers=HEADERS, timeout=20)
            if res.status_code != 200:
                print(f"  Error for topic {topic}: Status {res.status_code}")
                continue

            data = res.json()
            repos = data.get("items", [])
            print(f"  Topic [{topic:20}] >> Found {len(repos)} repos")

            for rank, repo in enumerate(repos, 1):
                try:
                    doc = {
                        "source": "api.github.com",
                        "rank": rank,
                        "name": repo.get("full_name", "N/A"),
                        "description": repo.get("description", "N/A"),
                        "language": repo.get("language", "N/A"),
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "watchers": repo.get("watchers_count", 0),
                        "open_issues": repo.get("open_issues_count", 0),
                        "topic": topic,
                        "created_at": repo.get("created_at", "N/A"),
                        "updated_at": repo.get("updated_at", "N/A"),
                        "scraped_at": datetime.now()
                    }
                    col.insert_one(doc)
                    saved += 1
                except:
                    continue

        except Exception as e:
            print(f"  Error for topic {topic}: {e}")
            continue

    print(f"  Total saved: {saved} top repositories\n")
    return saved

if __name__ == "__main__":
    collect()