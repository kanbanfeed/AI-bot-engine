from api.spear_api import app
from modules.thread_finder import run_thread_finder
from modules.spear_caller import call_spear_api
from modules.comment_builder import build_comment
from modules.poster import post_comment
from modules.response_monitor import check_for_responses

from db.queries import get_account_by_site

def run_engine():
    print("\n[ENGINE STARTED]\n")

    results = run_thread_finder()

    for site, threads in results.items():

        if not threads:
            print(f"No threads for {site}")
            continue

        account = get_account_by_site(site)

        if not account:
            print(f"No account for {site}")
            continue

        for thread in threads[:1]:  # limit per run

            print(f"\n[THREAD] {thread['url']}")

            phase_ii = call_spear_api(thread)

            if not phase_ii:
                print("Spear failed")
                continue

            comment_data = build_comment(thread, phase_ii, account)

            success, error = post_comment(site, thread, comment_data)

            print(f"Result → {success}, {error}")

    #  Run response monitor after posting
    check_for_responses()

    print("\n[ENGINE COMPLETE]\n")


if __name__ == "__main__":
    run_engine()