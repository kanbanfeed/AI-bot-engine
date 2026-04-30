from modules.poster import post_comment

#  USE SAFE TEST THREAD
thread = {
    "url": "https://www.reddit.com/r/test/comments/1/",  # safe subreddit
    "title": "Test thread",
    "selftext": "Testing bot"
}

comment_data = {
    "comment": "Test comment from bot. Ignore.",
    "opener": "test",
    "closer": "test"
}

#  USE ONLY ONE SITE
site = "spearprotocol"

result, error = post_comment(site, thread, comment_data)

print("\nRESULT:", result)
print("ERROR:", error)