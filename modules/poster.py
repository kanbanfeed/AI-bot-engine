import time
from datetime import datetime, timedelta
import praw

from db.queries import (
    insert_action,
    update_last_post_time,
    get_account_daily_post_count,
    get_account_by_site,
    get_global_config
)


# =========================
# DAILY LIMIT CHECK
# =========================
def check_daily_limit(account):
    config = get_global_config()
    karma = account.get("karma_points", 0)

    if karma < 25:
        limit = int(config.get("karma_tier_1_limit"))
    elif karma < 50:
        limit = int(config.get("karma_tier_2_limit"))
    elif karma < 75:
        limit = int(config.get("karma_tier_3_limit"))
    elif karma < 100:
        limit = int(config.get("karma_tier_4_limit"))
    elif karma < 125:
        limit = int(config.get("karma_tier_5_limit"))
    elif karma < 150:
        limit = int(config.get("karma_tier_6_limit"))
    elif karma < 175:
        limit = int(config.get("karma_tier_7_limit"))
    elif karma < 200:
        limit = int(config.get("karma_tier_8_limit"))
    else:
        limit = int(config.get("karma_tier_9_limit"))

    posts_today = get_account_daily_post_count(account["account_id"])
    return posts_today < limit


# =========================
# POST DELAY CHECK
# =========================
def check_post_delay(account):
    config = get_global_config()
    min_minutes = int(config.get("min_minutes_between_posts"))

    last_post = account.get("last_post_time")

    if not last_post:
        return True

    return datetime.utcnow() - last_post >= timedelta(minutes=min_minutes)


# =========================
# REAL REDDIT POST
# =========================
# def post_to_reddit(thread_url, comment, account):
#     try:
#         import praw

#         reddit = praw.Reddit(
#             client_id="dummy",
#             client_secret="dummy",
#             username=account["username"],
#             password=account["password"],
#             user_agent=f"{account['site']}_engine_v1"
#         )

#         submission = reddit.submission(url=thread_url)

#         print(f"\n[POSTING] {account['username']} -> {thread_url}")

#         submission.reply(comment)

#         time.sleep(5)

#         return True, None

#     except Exception as e:
#         return False, str(e)

def post_to_reddit(thread_url, comment, account):
    print(f"\n[SIMULATED POST] {account['username']} -> {thread_url}")
    print(comment[:120], "...\n")

    return True, "pending_post"

# =========================
# MAIN FUNCTION
# =========================
def post_comment(site, thread, comment_data):
    account = get_account_by_site(site)

    if not account:
        return False, "No account found"

    if not check_daily_limit(account):
        return False, "Daily limit reached"

    if not check_post_delay(account):
        return False, "Post delay not met"

    success, error = post_to_reddit(
        thread["url"],
        comment_data["comment"],
        account
    )

    insert_action({
        "account_id": account["account_id"],
        "platform": "reddit",
        "thread_url": thread["url"],
        "comment_text": comment_data["comment"],
        "opener_used": comment_data["opener"],
        "closer_used": comment_data["closer"],
        "round_number": 1,
        "posted_ok": False,
        "error_message": "pending_post"
    
    })

    if success:
        update_last_post_time(account["account_id"])

    return success, error