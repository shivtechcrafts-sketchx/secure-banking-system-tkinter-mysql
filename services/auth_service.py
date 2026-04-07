import bcrypt
from db.connection import get_connection

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password, account_id FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        stored_hash = result[0].encode()

        if bcrypt.checkpw(password.encode(), stored_hash):
            return result[1]

    return None