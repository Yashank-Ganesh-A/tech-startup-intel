import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.db import get_col

def process():
    print("[PROCESSING] Cleaning & enriching all collections...\n")

    col = get_col("github_trending")
    for doc in col.find({}):
        try:
            col.update_one({"_id": doc["_id"]}, {"$set": {
                "stars_numeric": int(doc.get("stars", 0)),
                "forks_numeric": int(doc.get("forks", 0)),
                "is_processed": True
            }})
        except:
            continue
    print("  [OK] github_trending processed")

    col = get_col("github_toprepos")
    for doc in col.find({}):
        try:
            col.update_one({"_id": doc["_id"]}, {"$set": {
                "stars_numeric": int(doc.get("stars", 0)),
                "forks_numeric": int(doc.get("forks", 0)),
                "is_processed": True
            }})
        except:
            continue
    print("  [OK] github_toprepos processed")

    col = get_col("hackernews")
    for doc in col.find({}):
        try:
            col.update_one({"_id": doc["_id"]}, {"$set": {
                "points_numeric": int(doc.get("points", 0)),
                "comments_numeric": int(doc.get("comments", 0)),
                "engagement_score": int(doc.get("points", 0)) + int(doc.get("comments", 0)),
                "is_processed": True
            }})
        except:
            continue
    print("  [OK] hackernews processed")

    col = get_col("pypi_packages")
    for doc in col.find({}):
        try:
            col.update_one({"_id": doc["_id"]}, {"$set": {"is_processed": True}})
        except:
            continue
    print("  [OK] pypi_packages processed")

    print("\n[DONE] All collections processed successfully!")

if __name__ == "__main__":
    process()