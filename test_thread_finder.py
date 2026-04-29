from modules.thread_finder import run_thread_finder

def print_results(results):
    for site, threads in results.items():
        print(f"\n===== SITE: {site} =====")

        if not threads:
            print("No threads found")
            continue

        for i, t in enumerate(threads, 1):
            print(f"\n{i}. {t['url']}")
            print(f"   Comments: {t['comments']}")
            print(f"   Velocity: {round(t['velocity'], 2)}")
            safe_title = t['title'].encode("utf-8", "ignore").decode("utf-8")
            print(f"   Title: {safe_title[:80]}")
            safe_url = t['url'].encode("utf-8", "ignore").decode("utf-8")
            print(f"\n{i}. {safe_url}")

if __name__ == "__main__":
    results = run_thread_finder()
    print_results(results)