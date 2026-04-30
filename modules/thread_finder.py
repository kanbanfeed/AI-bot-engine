import requests
import time
from datetime import datetime, timedelta

from db.queries import get_all_sites, get_site_config, thread_already_processed


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


# =========================
# HELPER — TIME FILTER
# =========================
def is_within_days(created_utc, max_days):
    post_time = datetime.utcfromtimestamp(created_utc)
    return post_time >= datetime.utcnow() - timedelta(days=max_days)


# =========================
# HELPER — COMMENT VELOCITY
# =========================
def calculate_velocity(num_comments, created_utc):
    hours = (datetime.utcnow() - datetime.utcfromtimestamp(created_utc)).total_seconds() / 3600
    return num_comments / hours if hours > 0 else 0


# =========================
# FETCH REDDIT THREADS
# =========================
def fetch_reddit_threads(subreddit, keyword):
    url = f"https://www.reddit.com/r/{subreddit}/search.json"

    params = {
        "q": keyword,
        "sort": "new",
        "t": "week",
        "limit": 100
    }

    for attempt in range(3):
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("children", [])

            elif response.status_code == 429:
                time.sleep(5 * (attempt + 1))  # exponential backoff

            else:
                return []

        except Exception:
            time.sleep(2)

    return []
# =========================
# MAIN FUNCTION
# =========================
def run_thread_finder():
    results = {}

    sites = get_all_sites()

    for site in sites:
        config = get_site_config(site)

        # Skip non-reddit sites
        if config.get("platform") not in ["reddit", "both"]:
            continue

        if config.get("active") != "true":
            continue
        seen_urls = set()
        subreddits = [s.strip() for s in config.get("targets", "").split(",") if s.strip()]
        keywords = [k.strip() for k in config.get("keywords", "").split(",") if k.strip()]

        min_comments = int(config.get("min_comments", 0))
        max_comments = int(config.get("max_comments", 100000))
        thread_age_days = int(config.get("thread_age_days", 7))

        collected_threads = []

        for subreddit in subreddits:
            for keyword in keywords:

                threads = fetch_reddit_threads(subreddit.strip(), keyword.strip())

                for t in threads:
                    data = t.get("data", {})

                    permalink = data.get("permalink")
                    if not permalink:
                        continue

                    thread_url = "https://www.reddit.com" + permalink

                    # DUPLICATE CHECK (same run)
                    if thread_url in seen_urls:
                        continue

                    seen_urls.add(thread_url)
                    num_comments = data.get("num_comments", 0)
                    created_utc = data.get("created_utc", 0)
                    if not created_utc:
                        continue

                    # FILTERS
                    if not is_within_days(created_utc, thread_age_days):
                        continue

                    if num_comments < min_comments or num_comments > max_comments:
                        continue

                    if thread_already_processed(thread_url):
                        continue

                    velocity = calculate_velocity(num_comments, created_utc)

                    collected_threads.append({
                        "url": thread_url,
                        "title": data.get("title"),
                        "selftext": data.get("selftext", ""),
                        "comments": num_comments,
                        "velocity": velocity,
                        "created_utc": created_utc
                    })

                time.sleep(2)  # avoid rate limit

        # SORT BY VELOCITY
        sorted_threads = sorted(collected_threads, key=lambda x: x["velocity"], reverse=True)

        # TOP 3 ONLY
        results[site] = sorted_threads[:3]

    return results