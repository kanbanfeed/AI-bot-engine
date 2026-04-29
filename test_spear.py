from modules.spear_caller import call_spear_api

thread = {
    "url": "test",
    "title": "I am stuck in my job and underpaid",
    "selftext": "My manager is not promoting me and I feel lost"
}

result = call_spear_api(thread)

print("\nPHASE II:\n", result)