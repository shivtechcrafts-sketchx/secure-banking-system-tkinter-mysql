from db.connection import get_connection

def get_balance(acc_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_id=%s", (acc_id,))
    bal = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return bal


def deposit(acc_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE accounts SET balance=balance+%s WHERE account_id=%s", (amount, acc_id))
    cursor.execute("INSERT INTO transactions(account_id,type,amount) VALUES(%s,'DEPOSIT',%s)", (acc_id, amount))

    conn.commit()
    cursor.close()
    conn.close()


def withdraw(acc_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_id=%s", (acc_id,))
    bal = cursor.fetchone()[0]

    if bal < amount:
        cursor.close()
        conn.close()
        return "Insufficient Balance"

    cursor.execute("UPDATE accounts SET balance=balance-%s WHERE account_id=%s", (amount, acc_id))
    cursor.execute("INSERT INTO transactions(account_id,type,amount) VALUES(%s,'WITHDRAW',%s)", (acc_id, amount))

    conn.commit()
    cursor.close()
    conn.close()
    return "Success"


def transfer_money(sender_id, receiver_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_id=%s", (sender_id,))
        sender_balance = cursor.fetchone()[0]

        if sender_balance < amount:
            return "Insufficient Balance"

        cursor.execute("UPDATE accounts SET balance=balance-%s WHERE account_id=%s", (amount, sender_id))
        cursor.execute("UPDATE accounts SET balance=balance+%s WHERE account_id=%s", (amount, receiver_id))

        cursor.execute("INSERT INTO transactions(account_id,type,amount) VALUES(%s,'TRANSFER_OUT',%s)", (sender_id, amount))
        cursor.execute("INSERT INTO transactions(account_id,type,amount) VALUES(%s,'TRANSFER_IN',%s)", (receiver_id, amount))

        conn.commit()
        return "Success"

    except:
        conn.rollback()
        return "Failed"

    finally:
        cursor.close()
        conn.close()