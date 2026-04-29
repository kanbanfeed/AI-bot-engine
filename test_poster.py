from modules.poster import post_comment

thread = {
    "url": "https://reddit.com/test"
}

comment_data = {
    "comment": "Test comment",
    "opener": "Test opener",
    "closer": "Test closer"
}

result, error = post_comment("careduel", thread, comment_data)

print(result, error)