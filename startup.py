from collectors.github_trending import collect as collect_trending
from collectors.github_toprepos import collect as collect_toprepos
from collectors.hackernews import collect as collect_hn
from collectors.pypi_packages import collect as collect_pypi
from insights.process import process
from insights.dashboard import run
from datetime import datetime

if __name__ == "__main__":
    print("#" * 70)
    print("## TECH & STARTUP INTELLIGENCE SYSTEM")
    print("## Collecting, Processing & Analyzing Tech Data")
    print(f"## Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#" * 70)

    print("\n[PHASE 1] DATA COLLECTION")
    print("-" * 70)
    collect_trending()
    collect_toprepos()
    collect_hn()
    collect_pypi()

    print("\n[PHASE 2] DATA PROCESSING")
    print("-" * 70)
    process()

    print("\n[PHASE 3] INTELLIGENCE DASHBOARD")
    print("-" * 70)
    run()

    print(f"\nSystem completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")