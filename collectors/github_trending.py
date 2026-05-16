import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.db import get_col
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9"
}

LANGUAGES = ["python", "javascript", "typescript", "go", "rust"]

def collect():
    col = get_col("github_trending")
    col.drop()
    saved = 0

    print("[COLLECTING] GitHub Trending Repositories...")

    for lang in LANGUAGES:
        url = f"https://github.com/trending/{lang}?since=weekly"
        try:
            res = requests.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(res.text, "lxml")
            repos = soup.find_all("article", class_="Box-row")
            print(f"  Language [{lang:12}] >> Found {len(repos)} repos")

            for rank, repo in enumerate(repos, 1):
                try:
                    name_tag = repo.find("h2")
                    name = name_tag.get_text(strip=True).replace("\n", "").replace(" ", "") if name_tag else "N/A"

                    desc_tag = repo.find("p")
                    desc = desc_tag.get_text(strip=True) if desc_tag else "N/A"

                    stars_tag = repo.find("a", href=lambda x: x and "stargazers" in str(x))
                    stars_text = stars_tag.get_text(strip=True).replace(",", "") if stars_tag else "0"
                    try:
                        stars = int(stars_text.replace("k", "000").replace(".", ""))
                    except:
                        stars = 0

                    forks_tag = repo.find("a", href=lambda x: x and "forks" in str(x))
                    forks_text = forks_tag.get_text(strip=True).replace(",", "") if forks_tag else "0"
                    try:
                        forks = int(forks_text)
                    except:
                        forks = 0

                    lang_tag = repo.find("span", itemprop="programmingLanguage")
                    repo_lang = lang_tag.get_text(strip=True) if lang_tag else lang

                    doc = {
                        "source": "github.com/trending",
                        "rank": rank,
                        "name": name,
                        "description": desc,
                        "language": repo_lang,
                        "stars": stars,
                        "forks": forks,
                        "trending_category": lang,
                        "scraped_at": datetime.now()
                    }
                    col.insert_one(doc)
                    saved += 1
                except:
                    continue

        except Exception as e:
            print(f"  Error for {lang}: {e}")
            continue

    print(f"  Total saved: {saved} trending repositories\n")
    return saved

if __name__ == "__main__":
    collect()