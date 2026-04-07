from db.connection import get_connection


# =========================
# GET ALL USERS
# =========================
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.user_id, u.username, a.account_id, a.account_holder, a.balance
        FROM users u
        JOIN accounts a ON u.account_id = a.account_id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =========================
# GET ALL TRANSACTIONS
# =========================
def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.trans_id, t.account_id, t.type, t.amount, t.created_at
        FROM transactions t
        ORDER BY t.created_at DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =========================
# UPDATE BALANCE (ADMIN FORCE)
# =========================
def update_balance(account_id, new_balance):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE accounts
        SET balance = %s
        WHERE account_id = %s
    """, (new_balance, account_id))

    conn.commit()

    cursor.close()
    conn.close()

    return True


# =========================
# DELETE USER
# =========================
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    # First get account_id
    cursor.execute("SELECT account_id FROM users WHERE user_id=%s", (user_id,))
    result = cursor.fetchone()

    if not result:
        return False

    acc_id = result[0]

    # Delete transactions
    cursor.execute("DELETE FROM transactions WHERE account_id=%s", (acc_id,))

    # Delete user
    cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))

    # Delete account
    cursor.execute("DELETE FROM accounts WHERE account_id=%s", (acc_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return True


# =========================
# CREATE NEW USER + ACCOUNT
# =========================
def create_user(username, password, holder_name, balance):
    conn = get_connection()
    cursor = conn.cursor()

    # Create account
    cursor.execute("""
        INSERT INTO accounts (account_holder, balance)
        VALUES (%s, %s)
    """, (holder_name, balance))

    acc_id = cursor.lastrowid

    # Create user
    cursor.execute("""
        INSERT INTO users (username, password, account_id)
        VALUES (%s, %s, %s)
    """, (username, password, acc_id))

    conn.commit()

    cursor.close()
    conn.close()

    return acc_id


# =========================
# SEARCH USER
# =========================
def search_user(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.user_id, u.username, a.account_holder, a.balance
        FROM users u
        JOIN accounts a ON u.account_id = a.account_id
        WHERE u.username LIKE %s OR a.account_holder LIKE %s
    """, (f"%{keyword}%", f"%{keyword}%"))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data