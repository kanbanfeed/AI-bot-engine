from db.connection import Database

# =========================
# GLOBAL CONFIG
# =========================
def get_global_config():
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT key, value FROM config WHERE site = 'global'"
    )

    config = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.close()
    Database.release_connection(conn)

    return config
# =========================
# CONFIG QUERIES
# =========================

def get_config_value(site, key):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM config WHERE site = %s AND key = %s",
        (site, key)
    )
    result = cursor.fetchone()

    cursor.close()
    Database.release_connection(conn)

    return result[0] if result else None


def get_all_sites():
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT site FROM config WHERE site != 'global'")
    sites = [row[0] for row in cursor.fetchall()]

    cursor.close()
    Database.release_connection(conn)

    return sites


def get_site_config(site):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT key, value FROM config WHERE site = %s",
        (site,)
    )

    config = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.close()
    Database.release_connection(conn)

    return config


# =========================
# ACCOUNTS QUERIES
# =========================

def get_active_accounts():
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE status = 'active'")
    rows = cursor.fetchall()

    cursor.close()
    Database.release_connection(conn)

    return rows


def update_last_post_time(account_id):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE accounts SET last_post_time = NOW() WHERE account_id = %s",
        (account_id,)
    )

    conn.commit()
    cursor.close()
    Database.release_connection(conn)


def update_opener_position(account_id, position):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE accounts SET opener_position = %s WHERE account_id = %s",
        (position, account_id)
    )

    conn.commit()
    cursor.close()
    Database.release_connection(conn)


def update_closer_position(account_id, position):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE accounts SET closer_position = %s WHERE account_id = %s",
        (position, account_id)
    )

    conn.commit()
    cursor.close()
    Database.release_connection(conn)


# =========================
# ACTIONS QUERIES
# =========================

def insert_action(data):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO actions (
            account_id, platform, thread_url, comment_text,
            opener_used, closer_used, round_number,
            posted_ok, error_message, elevation_triggered
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING action_id
    """, (
        data.get("account_id"),
        data.get("platform"),
        data.get("thread_url"),
        data.get("comment_text"),
        data.get("opener_used"),
        data.get("closer_used"),
        data.get("round_number"),
        data.get("posted_ok"),
        data.get("error_message"),
        data.get("elevation_triggered", False)
    ))

    action_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    Database.release_connection(conn)

    return action_id


def thread_already_processed(thread_url):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM actions WHERE thread_url = %s LIMIT 1",
        (thread_url,)
    )

    exists = cursor.fetchone() is not None

    cursor.close()
    Database.release_connection(conn)

    return exists


# =========================
# ENGAGEMENT QUERIES
# =========================

def insert_engagement(data):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO engagement (
            action_id, upvotes, replies_to_our_comment,
            thread_comments_before, thread_comments_after
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        data.get("action_id"),
        data.get("upvotes"),
        data.get("replies"),
        data.get("before"),
        data.get("after")
    ))

    conn.commit()
    cursor.close()
    Database.release_connection(conn)

# =========================
# ERROR LOGGING (REQUIRED)
# =========================
def log_action_error(account_id, thread_url, error_message):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO actions (
            account_id, platform, thread_url,
            comment_text, opener_used, closer_used,
            round_number, posted_ok, error_message, elevation_triggered
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        account_id,
        "reddit",
        thread_url,
        None,
        None,
        None,
        1,
        False,
        error_message,
        False
    ))

    conn.commit()
    cursor.close()
    Database.release_connection(conn)
# =========================
# FLAGS
# =========================

def insert_flag(data):

    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO flags (
            account_id, flag_type, flag_message, status, drone_action_taken
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        data.get("account_id"),
        data.get("flag_type"),
        data.get("flag_message"),
        data.get("status"),
        data.get("drone_action_taken")
    ))

    conn.commit()
    cursor.close()
    Database.release_connection(conn)



def get_account_by_site(site):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM accounts
        WHERE site = %s AND status = 'active'
        LIMIT 1
    """, (site,))

    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    Database.release_connection(conn)

    if not row:
        return None

    return dict(zip(columns, row))


# =========================
# DAILY POST COUNT
# =========================
def get_account_daily_post_count(account_id):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM actions
        WHERE account_id = %s
        AND posted_ok = TRUE
        AND timestamp >= CURRENT_DATE
    """, (account_id,))

    count = cursor.fetchone()[0]

    cursor.close()
    Database.release_connection(conn)

    return count
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM accounts
        WHERE site = %s AND status = 'active'
        LIMIT 1
    """, (site,))

    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    Database.release_connection(conn)

    if not row:
        return None

    return dict(zip(columns, row))


def get_account_daily_post_count(account_id):
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM actions
        WHERE account_id = %s
        AND posted_ok = TRUE
        AND timestamp >= CURRENT_DATE
    """, (account_id,))

    count = cursor.fetchone()[0]

    cursor.close()
    Database.release_connection(conn)

    return count