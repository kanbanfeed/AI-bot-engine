from db.queries import (
    get_config_value,
    update_opener_position,
    update_closer_position
)


# =========================
# GET OPENER
# =========================
def get_next_opener(account):
    current_pos = account["opener_position"] or 1

    opener = get_config_value("global", f"opener_{current_pos}")

    next_pos = current_pos + 1 if current_pos < 15 else 1
    update_opener_position(account["account_id"], next_pos)

    return opener


# =========================
# GET CLOSER
# =========================
def get_next_closer(account):
    current_pos = account["closer_position"] or 1

    closer = get_config_value("global", f"closer_{current_pos}")

    next_pos = current_pos + 1 if current_pos < 15 else 1
    update_closer_position(account["account_id"], next_pos)

    return closer


# =========================
# BUILD COMMENT
# =========================
def build_comment(thread, phase_ii, account):
    opener = get_next_opener(account)
    closer = get_next_closer(account)

    comment = f"{opener}\n\n{phase_ii}\n\n{closer}"

    return {
        "comment": comment,
        "opener": opener,
        "closer": closer
    }


# =========================
# VALIDATE COMMENT
# =========================
def validate_comment(comment, opener, closer):
    if not comment:
        return False, "Empty comment"

    if not opener or not closer:
        return False, "Missing opener/closer"

    # Check structure
    parts = comment.split("\n\n")

    if len(parts) != 3:
        return False, "Invalid structure"

    if parts[0].strip() != opener.strip():
        return False, "Opener mismatch"

    if parts[-1].strip() != closer.strip():
        return False, "Closer mismatch"

    # Phase II length check
    phase_ii = parts[1].strip()
    if len(phase_ii.split()) < 50:
        return False, "Phase II too short"

    # Error words check
    banned = ["error", "exception", "traceback", "failed", "NoneType", "null", "undefined", "500"]
    lower_comment = comment.lower()

    for word in banned:
        if word in lower_comment:
            return False, f"Banned word found: {word}"

    return True, None


# =========================
# MAIN FUNCTION
# =========================
def create_comment(account, phase_ii):
    comment, opener, closer = build_comment(account, phase_ii)

    is_valid, error = validate_comment(comment, opener, closer)

    if not is_valid:
        return None, error

    return {
        "comment": comment,
        "opener": opener,
        "closer": closer
    }, None