import tkinter as tk
from services.auth_service import login_user
from ui.dashboard_ui import open_dashboard


def open_login(root):
    for w in root.winfo_children():
        w.destroy()

    root.configure(bg="#1e1e2e")

    # =======================
    # SIDEBAR
    # =======================
    sidebar = tk.Frame(root, bg="#334155", width=250)
    sidebar.pack(side="left", fill="y")

    # TOP
    top = tk.Frame(sidebar, bg="#334155")
    top.pack(pady=40)

    tk.Label(top, text="🏠 Bank App",
             font=("Segoe UI", 18, "bold"),
             fg="white", bg="#334155").pack()

    tk.Label(top,
             text="Secure Banking System\nPython + MySQL",
             font=("Segoe UI", 10),
             fg="#cbd5f5", bg="#334155").pack(pady=10)

    # PUSH DOWN
    tk.Frame(sidebar, bg="#334155").pack(expand=True)

    # BOTTOM
    bottom = tk.Frame(sidebar, bg="#334155")
    bottom.pack(pady=20)

    tk.Label(bottom,
             text="Created by Shiv 💻",
             font=("Segoe UI", 10),
             fg="#94a3b8", bg="#334155").pack()

    tk.Label(bottom,
             text="© 2026",
             font=("Segoe UI", 8),
             fg="#64748b", bg="#334155").pack()

    # =======================
    # LOGIN CARD
    # =======================
    main = tk.Frame(root, bg="#1e1e2e")
    main.pack(side="right", expand=True, fill="both")

    card = tk.Frame(main, bg="#2a2a40", padx=30, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(card, text="Login",
             font=("Segoe UI", 18, "bold"),
             fg="white", bg="#2a2a40").pack(pady=10)

    # USERNAME
    tk.Label(card, text="Username",
             fg="#cbd5f5", bg="#2a2a40").pack(anchor="w")
    user = tk.Entry(card, width=25)
    user.pack(pady=5)

    # PASSWORD
    tk.Label(card, text="Password",
             fg="#cbd5f5", bg="#2a2a40").pack(anchor="w")
    pwd = tk.Entry(card, width=25, show="*")
    pwd.pack(pady=5)

    # SHOW / HIDE
    def toggle():
        pwd.config(show="" if pwd.cget("show") == "*" else "*")

    tk.Button(card, text="Show", command=toggle).pack(pady=5)

    msg = tk.Label(card, text="", fg="red", bg="#2a2a40")
    msg.pack()

    # LOGIN FUNCTION
    def do_login():
        acc_id = login_user(user.get(), pwd.get())

        if acc_id:
            open_dashboard(root, acc_id)
        else:
            msg.config(text="Invalid Login")

    tk.Button(card, text="Login",
              bg="#4f46e5", fg="white",
              command=do_login).pack(pady=10)