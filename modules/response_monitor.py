import random
from db.queries import get_pending_actions, mark_action_responded


# =========================
# SIMULATE RESPONSE CHECK
# =========================
def check_for_responses():
    print("\n[RESPONSE MONITOR STARTED]\n")

    actions = get_pending_actions()

    if not actions:
        print("No pending actions")
        return

    for action in actions:
        action_id = action["action_id"]
        thread_url = action["thread_url"]

        print(f"Checking responses for: {thread_url}")

        # SIMULATE response (random)
        responded = random.choice([True, False])

        if responded:
            print("-> Response detected")

            mark_action_responded(action_id)

        else:
            print("-> No response")

    print("\n[RESPONSE MONITOR COMPLETE]\n")