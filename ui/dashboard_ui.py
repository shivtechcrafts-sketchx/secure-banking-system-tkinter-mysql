import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt

from services.banking_service import get_balance, deposit, withdraw, transfer_money
from db.connection import get_connection
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def open_dashboard(root, acc_id):

    # =========================
    # CLEAR SCREEN
    # =========================
    for w in root.winfo_children():
        w.destroy()

    root.geometry("1100x600")

    # =========================
    # THEME
    # =========================
    theme = {"bg": "#082456", "fg": "white"}

    def toggle_theme():
        if theme["bg"] == "#0b1a33":
            theme["bg"] = "white"
            theme["fg"] = "black"

        elif theme["bg"] == "white":
            theme["bg"] = "#0b1a33"
            theme["fg"] = "skyblue"
        else:
            theme["bg"] = "#0b1a33"
            theme["fg"] = "white"

        root.configure(bg=theme["bg"])
        main.configure(bg=theme["bg"])

    # =========================
    # USER DATA
    # =========================
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT account_holder FROM accounts WHERE account_id=%s", (acc_id,))
    user = cursor.fetchone()
    username = user[0] if user else "User"

    cursor.close()
    conn.close()

    login_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # =========================
    # TOP BAR
    # =========================
    top = tk.Frame(root, bg="#12264d", height=60)
    top.pack(fill="x")

    tk.Label(top, text=f"Welcome {username}", bg="#12264d",
             fg="white", font=("Arial", 14, "bold")).pack(side="left", padx=20)

    right = tk.Frame(top, bg="#12264d")
    right.pack(side="right", padx=20)

    def logout():
        from ui.login_ui import open_login
        open_login(root)

    tk.Button(right, text="Logout", bg="#ff4d4d",
              fg="white", command=logout).pack(anchor="e")

    tk.Label(right, text=f"Login: {login_time}", bg="#12264d",
             fg="#ccc", font=("Arial", 9)).pack(anchor="e")

    # =========================
    # SIDEBAR
    # =========================
    sidebar = tk.Frame(root, bg="#000000", width=200)
    sidebar.pack(side="left", fill="y")

    # =========================
    # MAIN AREA
    # =========================
    main = tk.Frame(root, bg=theme["bg"])
    main.pack(side="right", expand=True, fill="both")

    # =========================
    # COMMON FUNCTIONS
    # =========================
    def clear_main():
        for w in main.winfo_children():
            w.destroy()

    def refresh_balance(label):
        bal = get_balance(acc_id)
        label.config(text=f"₹ {bal:.2f}")

    # =========================
    # DASHBOARD
    # =========================
    def show_dashboard():
        clear_main()

        tk.Label(main, text="Bank Balance", bg=theme["bg"],
                 fg=theme["fg"], font=("Arial", 22, "bold")).pack(pady=20)

        balance_label = tk.Label(main, text="₹ 0.00",
                                 bg=theme["bg"], fg="#E47070",
                                 font=("Arial", 28, "bold"))
        balance_label.pack(pady=30)

        refresh_balance(balance_label)

    # =========================
    # TRANSACTIONS + SEARCH
    # =========================
    def show_transactions():
        clear_main()

        tk.Label(main, text="Transactions", bg=theme["bg"],
                 fg=theme["fg"], font=("Arial", 18)).pack(pady=10)

        search = tk.Entry(main)
        search.pack(pady=5)

        result_frame = tk.Frame(main, bg=theme["bg"])
        result_frame.pack()

        def load_data(filter_val=""):
            for w in result_frame.winfo_children():
                w.destroy()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT type, amount, created_at
                FROM transactions
                WHERE account_id=%s AND type LIKE %s
                ORDER BY created_at DESC
            """, (acc_id, f"%{filter_val}%"))

            rows = cursor.fetchall()

            for r in rows:
                tk.Label(result_frame,
                         text=f"{r[0]} | ₹{r[1]} | {r[2]}",
                         bg=theme["bg"], fg=theme["fg"]).pack()

            cursor.close()
            conn.close()

        tk.Button(main, text="Search",
                  command=lambda: load_data(search.get())).pack()

        load_data()

    # =========================
    # DEPOSIT
    # =========================
    def show_deposit():
        clear_main()

        tk.Label(main, text="Deposit", bg=theme["bg"],
                 fg=theme["fg"], font=("Arial", 18)).pack(pady=10)

        amt = tk.Entry(main)
        amt.pack(pady=10)

        def do_deposit():
            try:
                deposit(acc_id, float(amt.get()))
                messagebox.showinfo("Success", "Deposited")
                show_dashboard()
            except:
                messagebox.showerror("Error", "Invalid input")

        tk.Button(main, text="Deposit", command=do_deposit).pack()

    # =========================
    # WITHDRAW
    # =========================
    def show_withdraw():
        clear_main()

        tk.Label(main, text="Withdraw", bg=theme["bg"],
                 fg=theme["fg"], font=("Arial", 18)).pack(pady=10)

        amt = tk.Entry(main)
        amt.pack(pady=10)

        def do_withdraw():
            try:
                withdraw(acc_id, float(amt.get()))
                messagebox.showinfo("Success", "Withdrawn")
                show_dashboard()
            except:
                messagebox.showerror("Error", "Invalid input")

        tk.Button(main, text="Withdraw", command=do_withdraw).pack()

    # =========================
    # TRANSFER
    # =========================
    def show_transfer():
        clear_main()

        tk.Label(main, text="Transfer", bg=theme["bg"],
                 fg=theme["fg"], font=("Arial", 18)).pack(pady=10)

        to = tk.Entry(main)
        to.insert(0, "Receiver ID")
        to.pack(pady=5)

        amt = tk.Entry(main)
        amt.insert(0, "Amount")
        amt.pack(pady=5)

        def do_transfer():
            try:
                transfer_money(acc_id, int(to.get()), float(amt.get()))
                messagebox.showinfo("Success", "Transferred")
                show_dashboard()
            except:
                messagebox.showerror("Error", "Invalid input")

        tk.Button(main, text="Transfer", command=do_transfer).pack()

    # =========================
    # ANALYTICS (GRAPH)
    # =========================
    def show_graph():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT type, amount FROM transactions WHERE account_id=%s", (acc_id,))
        data = cursor.fetchall()

        deposits = sum(x[1] for x in data if x[0] == "DEPOSIT")
        withdraws = sum(x[1] for x in data if x[0] == "WITHDRAW")

        plt.figure()
        plt.bar(["Deposit", "Withdraw"], [deposits, withdraws])
        plt.title("Analytics")
        plt.show()

        plt.figure()
        plt.pie([deposits, withdraws], labels=["Deposit", "Withdraw"], autopct="%0.2f%%")
        plt.title("Analytics")
        plt.show()

    # =========================
    # EXPORT PDF
    # =========================
    def export_pdf():
        doc = SimpleDocTemplate("statement.pdf")
        styles = getSampleStyleSheet()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT type, amount, created_at FROM transactions WHERE account_id=%s", (acc_id,))
        data = cursor.fetchall()

        content = []

        for d in data:
            content.append(Paragraph(f"{d[0]} - ₹{d[1]} - {d[2]}", styles["Normal"]))

        doc.build(content)

        messagebox.showinfo("Done", "PDF Exported")

    # =========================
    # SIDEBAR MENU
    # =========================
    def menu(text, cmd):
        return tk.Button(
            sidebar,
            text=text,
            bg="#000814",
            fg="white",
            font=("Arial", 12),
            bd=0,
            anchor="w",
            command=cmd
        )

    menu("🏠 Dashboard", show_dashboard).pack(fill="x", pady=5)
    menu("📄 Transactions", show_transactions).pack(fill="x", pady=5)
    menu("💰 Deposit", show_deposit).pack(fill="x", pady=5)
    menu("💸 Withdraw", show_withdraw).pack(fill="x", pady=5)
    menu("🔁 Transfer", show_transfer).pack(fill="x", pady=5)
    menu("📊 Analytics", show_graph).pack(fill="x", pady=5)
    menu("📄 Export PDF", export_pdf).pack(fill="x", pady=5)
    menu("🌙 Toggle Theme", toggle_theme).pack(fill="x", pady=5)

    # DEFAULT
    show_dashboard()