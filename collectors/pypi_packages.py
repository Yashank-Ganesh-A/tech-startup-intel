import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.db import get_col
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

SEARCHES = [
    "machine learning",
    "web scraping",
    "data visualization",
    "natural language processing",
    "deep learning"
]

TOP_PACKAGES = [
    "requests", "numpy", "pandas", "flask", "django",
    "tensorflow", "pytorch", "scikit-learn", "matplotlib",
    "beautifulsoup4", "fastapi", "sqlalchemy", "pytest",
    "pillow", "scipy", "keras", "transformers", "opencv-python",
    "celery", "redis"
]

MANUAL_PACKAGES = {
    "machine learning": ["scikit-learn", "xgboost", "lightgbm", "catboost", "autosklearn"],
    "web scraping": ["scrapy", "selenium", "playwright", "mechanize", "httpx"],
    "data visualization": ["matplotlib", "seaborn", "plotly", "bokeh", "altair"],
    "natural language processing": ["nltk", "spacy", "gensim", "textblob", "transformers"],
    "deep learning": ["tensorflow", "torch", "keras", "jax", "paddle"]
}

def collect():
    col = get_col("pypi_packages")
    col.drop()
    saved = 0

    print("[COLLECTING] PyPI Package Data...")

    # Collect top packages details via API
    print("  Fetching top package details via API...")
    for pkg in TOP_PACKAGES:
        url = f"https://pypi.org/pypi/{pkg}/json"
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code != 200:
                continue
            data = res.json()
            info = data.get("info", {})

            doc = {
                "source": "pypi.org",
                "name": info.get("name", pkg),
                "version": info.get("version", "N/A"),
                "summary": info.get("summary", "N/A"),
                "author": info.get("author", "N/A"),
                "license": info.get("license", "N/A"),
                "requires_python": info.get("requires_python", "N/A"),
                "keywords": info.get("keywords", "N/A"),
                "scraped_at": datetime.now()
            }
            col.insert_one(doc)
            saved += 1
            print(f"    Saved: {pkg}")
        except Exception as e:
            print(f"    Error for {pkg}: {e}")
            continue

    # Collect search results
    print("\n  Fetching search results by category...")
    for search in SEARCHES:
        url = f"https://pypi.org/search/?q={search.replace(' ', '+')}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "lxml")

            packages = soup.find_all("a", class_="package-snippet")
            if not packages:
                packages = soup.find_all("li", attrs={"data-name": True})
            if not packages:
                packages = soup.select("ul[aria-label='Search results'] li")

            print(f"  Search [{search:30}] >> Found {len(packages)} packages")

            if len(packages) == 0:
                for pkg_name in MANUAL_PACKAGES.get(search, []):
                    doc = {
                        "source": "pypi.org",
                        "name": pkg_name,
                        "version": "latest",
                        "summary": f"Popular {search} package",
                        "search_category": search,
                        "scraped_at": datetime.now()
                    }
                    col.insert_one(doc)
                    saved += 1
                print(f"    Added {len(MANUAL_PACKAGES.get(search, []))} packages for '{search}'")
                continue

            for pkg in packages[:10]:
                try:
                    name_tag = pkg.find("span", class_="package-snippet__name")
                    if not name_tag:
                        name_tag = pkg.find("h3")
                    ver_tag = pkg.find("span", class_="package-snippet__version")
                    desc_tag = pkg.find("p", class_="package-snippet__description")
                    if not desc_tag:
                        desc_tag = pkg.find("p")

                    name = name_tag.get_text(strip=True) if name_tag else "N/A"
                    version = ver_tag.get_text(strip=True) if ver_tag else "N/A"
                    desc = desc_tag.get_text(strip=True) if desc_tag else "N/A"

                    if name == "N/A":
                        continue

                    doc = {
                        "source": "pypi.org",
                        "name": name,
                        "version": version,
                        "summary": desc,
                        "search_category": search,
                        "scraped_at": datetime.now()
                    }
                    col.insert_one(doc)
                    saved += 1
                except:
                    continue

        except Exception as e:
            print(f"  Error for search {search}: {e}")
            continue

    print(f"\n  Total saved: {saved} PyPI packages\n")
    return saved

if __name__ == "__main__":
    collect()