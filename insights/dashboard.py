import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.db import get_col
from datetime import datetime

LINE = "#" * 70

def github_trending_report():
    print(f"\n{LINE}")
    print("## REPORT 1 >> TOP 10 TRENDING GITHUB REPOS THIS WEEK")
    print(LINE)
    col = get_col("github_trending")
    results = list(col.find(
        {"stars": {"$gt": 0}},
        {"name": 1, "language": 1, "stars": 1, "forks": 1, "description": 1}
    ).sort("stars", -1).limit(10))

    if results:
        for i, r in enumerate(results, 1):
            desc = str(r.get("description", ""))[:40]
            print(f"  {i:2}. {r.get('name','N/A'):45} | Lang: {r.get('language','N/A'):12} | Stars: {r.get('stars',0):6,} | Forks: {r.get('forks',0):5,}")
    else:
        print("  No data available")

def language_popularity():
    print(f"\n{LINE}")
    print("## REPORT 2 >> MOST POPULAR PROGRAMMING LANGUAGES (GITHUB)")
    print(LINE)
    col = get_col("github_toprepos")
    pipeline = [
        {"$match": {"language": {"$ne": "N/A", "$ne": None}}},
        {"$group": {
            "_id": "$language",
            "repo_count": {"$sum": 1},
            "total_stars": {"$sum": "$stars"},
            "avg_stars": {"$avg": "$stars"}
        }},
        {"$sort": {"total_stars": -1}},
        {"$limit": 10}
    ]
    results = list(col.aggregate(pipeline))
    if results:
        for i, r in enumerate(results, 1):
            print(f"  {i:2}. {str(r['_id']):20} | Repos: {r['repo_count']:3} | Total Stars: {r['total_stars']:>10,} | Avg Stars: {r['avg_stars']:>10,.0f}")
    else:
        print("  No data available")

def top_repos_by_topic():
    print(f"\n{LINE}")
    print("## REPORT 3 >> TOP REPOS BY TECH TOPIC (GITHUB API)")
    print(LINE)
    col = get_col("github_toprepos")
    pipeline = [
        {"$group": {
            "_id": "$topic",
            "total_repos": {"$sum": 1},
            "avg_stars": {"$avg": "$stars"},
            "total_stars": {"$sum": "$stars"}
        }},
        {"$sort": {"avg_stars": -1}}
    ]
    results = list(col.aggregate(pipeline))
    if results:
        for i, r in enumerate(results, 1):
            print(f"  {i:2}. {str(r['_id']):25} | Repos: {r['total_repos']:3} | Avg Stars: {r['avg_stars']:>10,.0f} | Total Stars: {r['total_stars']:>12,}")
    else:
        print("  No data available")

def hackernews_report():
    print(f"\n{LINE}")
    print("## REPORT 4 >> TOP 10 HACKERNEWS STORIES BY POINTS")
    print(LINE)
    col = get_col("hackernews")
    results = list(col.find(
        {"points_numeric": {"$gt": 0}},
        {"title": 1, "author": 1, "points_numeric": 1, "comments_numeric": 1, "query_tag": 1}
    ).sort("points_numeric", -1).limit(10))

    if results:
        for i, r in enumerate(results, 1):
            title = str(r.get("title", ""))[:50]
            print(f"  {i:2}. {title:52} | Points: {r.get('points_numeric',0):5} | Comments: {r.get('comments_numeric',0):4} | Tag: {r.get('query_tag','N/A')}")
    else:
        print("  No data available")

def hackernews_by_topic():
    print(f"\n{LINE}")
    print("## REPORT 5 >> HACKERNEWS STORIES COUNT & AVG POINTS BY TOPIC")
    print(LINE)
    col = get_col("hackernews")
    pipeline = [
        {"$group": {
            "_id": "$query_tag",
            "story_count": {"$sum": 1},
            "avg_points": {"$avg": "$points_numeric"},
            "total_points": {"$sum": "$points_numeric"},
            "avg_comments": {"$avg": "$comments_numeric"}
        }},
        {"$sort": {"avg_points": -1}}
    ]
    results = list(col.aggregate(pipeline))
    if results:
        for i, r in enumerate(results, 1):
            print(f"  {i:2}. {str(r['_id']):25} | Stories: {r['story_count']:3} | Avg Points: {r['avg_points']:7.1f} | Total Points: {r['total_points']:6} | Avg Comments: {r['avg_comments']:.1f}")
    else:
        print("  No data available")

def pypi_report():
    print(f"\n{LINE}")
    print("## REPORT 6 >> TOP PYTHON PACKAGES BY CATEGORY (PYPI)")
    print(LINE)
    col = get_col("pypi_packages")
    pipeline = [
        {"$match": {"search_category": {"$exists": True}}},
        {"$group": {
            "_id": "$search_category",
            "package_count": {"$sum": 1},
            "packages": {"$push": "$name"}
        }},
        {"$sort": {"package_count": -1}}
    ]
    results = list(col.aggregate(pipeline))
    if results:
        for i, r in enumerate(results, 1):
            pkgs = ", ".join(r.get("packages", [])[:5])
            print(f"  {i:2}. {str(r['_id']):35} | Packages: {r['package_count']:3} | Top: {pkgs[:50]}")
    else:
        print("  No data available")

def summary():
    print(f"\n{LINE}")
    print("## REPORT 7 >> DATABASE SUMMARY")
    print(LINE)
    collections = ["github_trending", "github_toprepos", "hackernews", "pypi_packages"]
    sources = [
        "github.com/trending       (Trending Repos)",
        "api.github.com            (Top Repos by Topic)",
        "hn.algolia.com            (HackerNews Stories)",
        "pypi.org                  (Python Packages)"
    ]
    total = 0
    for col_name, source in zip(collections, sources):
        count = get_col(col_name).count_documents({})
        total += count
        print(f"  {source:50} >> {count:4} records")
    print(f"\n  {'TOTAL RECORDS':50} >> {total:4}")
    print(f"  {'GENERATED AT':50} >> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def run():
    print(f"\n{LINE}")
    print("## TECH & STARTUP INTELLIGENCE DASHBOARD")
    print("## Data Management Project -- SRH University Hamburg")
    print(f"## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(LINE)

    github_trending_report()
    language_popularity()
    top_repos_by_topic()
    hackernews_report()
    hackernews_by_topic()
    pypi_report()
    summary()

    print(f"\n{LINE}")
    print("## ALL REPORTS GENERATED SUCCESSFULLY")
    print(LINE + "\n")

if __name__ == "__main__":
    run()