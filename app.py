import tkinter as tk
from ui.login_ui import open_login

root = tk.Tk()
root.title("Bank App")
root.geometry("1000x600")

open_login(root)

root.mainloop()