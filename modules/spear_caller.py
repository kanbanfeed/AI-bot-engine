import requests
import re

from db.queries import log_action_error, get_global_config


# =========================
# EXTRACT PHASE II
# =========================
def extract_phase_ii(full_text):
    try:
        # Normalize text
        text = full_text.replace("\r", "").strip()

        # Extract PHASE II
        match = re.search(
            r"PHASE II\s*(.*?)\s*PHASE III",
            text,
            re.DOTALL | re.IGNORECASE
        )

        if not match:
            return None

        phase_ii = match.group(1).strip()

        #  CLEANING (PRODUCTION FIXES)
        phase_ii = re.sub(r"Kill Point", "", phase_ii, flags=re.IGNORECASE)
        phase_ii = phase_ii.encode("utf-8", "ignore").decode("utf-8")
        phase_ii = re.sub(r"\n+", "\n", phase_ii)
        phase_ii = phase_ii.strip().replace("\r", "")

        return phase_ii

    except Exception:
        return None


# =========================
# VALIDATION
# =========================
def validate_phase_ii(text):
    if not text:
        return False, "Empty Phase II"

    if len(text.split()) < 50:
        return False, "Too short (<50 words)"

    banned = ["error", "exception", "traceback", "failed", "NoneType", "null", "undefined", "500"]
    lower_text = text.lower()

    for b in banned:
        if b in lower_text:
            return False, f"Contains banned word: {b}"

    # Basic English check (simple heuristic)
    if not re.search(r"[a-zA-Z]", text):
        return False, "Not English"

    return True, None


# =========================
# MAIN FUNCTION
# =========================
def call_spear_api(thread, account_id=None):
    """
    thread: {
        url, title, selftext
    }
    """

    config = get_global_config()

    endpoint = config.get("spear_api_endpoint")
    api_key = config.get("spear_api_key")

    # Combine title + body (ONLY content, no metadata)
    input_text = f"{thread.get('title', '')}\n\n{thread.get('selftext', '')}".strip()

    if not input_text:
        log_action_error(account_id, thread.get("url"), "Empty input text")
        return None

    try:
        response = requests.post(
            endpoint,
            json={"text": input_text},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            timeout=20
        )

        if response.status_code != 200:
            log_action_error(account_id, thread.get("url"), f"API failed: {response.status_code}")
            return None

        data = response.json()
        full_output = data.get("output", "")

        # Extract Phase II
        print("\n[DEBUG] FULL API OUTPUT:\n", full_output)

        phase_ii = extract_phase_ii(full_output)

        if not phase_ii:
            print("\n[ERROR] Phase II extraction failed")
            return None

        # Validate
        is_valid, error = validate_phase_ii(phase_ii)

        if not is_valid:
            log_action_error(account_id, thread.get("url"), error)
            return None

        return phase_ii

    except Exception as e:
        log_action_error(account_id, thread.get("url"), str(e))
        return None