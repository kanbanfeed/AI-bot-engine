from modules.thread_finder import run_thread_finder
from modules.spear_caller import call_spear_api
from modules.comment_builder import build_comment
from modules.poster import post_comment

from db.queries import get_account_by_site

print("\nRUNNING FULL ENGINE...\n")

# Run thread finder
results = run_thread_finder()

#  Use only one site
site = "spearprotocol"

threads = results.get(site, [])

if not threads:
    print("No threads found")
    exit()

#  Get account (IMPORTANT FIX)
account = get_account_by_site(site)

if not account:
    print("No account found for site")
    exit()

for thread in threads[:1]:   # only 1 thread

    print("\n[THREAD FOUND]")
    print(thread["url"])

    # STEP 1 — Spear API
    phase_ii = call_spear_api(thread)

    if not phase_ii:
        print("Spear failed")
        continue

    print("\n[PHASE II OUTPUT]")
    print(phase_ii)

    # STEP 2 — Build Comment (FIXED)
    comment_data = build_comment(thread, phase_ii, account)

    print("\n[COMMENT BUILT]")

    # STEP 3 — Post (mock or real)
    success, error = post_comment(site, thread, comment_data)

    print("\n[POST RESULT]")
    print("SUCCESS:", success)
    print("ERROR:", error)

    break  # run only once