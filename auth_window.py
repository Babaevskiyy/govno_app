import tkinter as tk
from tkinter import messagebox
from database import Database
from application_window import ApplicationWindow
from special_window import SpecialWindow
from datetime import datetime
from tkinter import ttk

class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Авторизация")
        self.master.configure(bg="#2C2F33")
        self.db = Database("users.db")

        self.container = tk.Frame(master, bg="#2C2F33")
        self.container.grid(row=0, column=0, padx=500, pady=250)

        self.label_username = tk.Label(self.container, text="Имя пользователя: ", bg="#2C2F33", fg="#FFFFFF", font="Tablón")
        self.label_username.grid(row=0, column=0, sticky="e")

        self.entry_username = tk.Entry(self.container, bg="#40444B", fg="#FFFFFF", insertbackground="#FFFFFF", relief=tk.FLAT, font="Tablón")
        self.entry_username.grid(row=0, column=1, sticky="w")

        self.label_password = tk.Label(self.container, text="Пароль: ", bg="#2C2F33", fg="#FFFFFF", font="Tablón")
        self.label_password.grid(row=1, column=0, sticky="e")

        self.entry_password = tk.Entry(self.container, show="*", bg="#40444B", fg="#FFFFFF", insertbackground="#FFFFFF", relief=tk.FLAT, font="Tablón")
        self.entry_password.grid(row=1, column=1, sticky="w")

        self.show_password_var = tk.BooleanVar()

        self.checkbox_show_password = tk.Checkbutton(self.container, text="Показать пароль", variable=self.show_password_var, command=self.toggle_password_visibility, bg="#2C2F33", fg="#FFFFFF", font="Tablón")
        self.checkbox_show_password.grid(row=2, columnspan=2)

        self.btn_login = tk.Button(self.container, text="Войти", command=self.login, bg="#7289DA", fg="#FFFFFF", relief=tk.FLAT, padx=10, pady=5, font="Tablón", width=20)
        self.btn_login.grid(row=3, columnspan=2)
        
        self.btn_login_image = tk.PhotoImage(file="button.png")  
        self.btn_login = tk.Button(self.container, image=self.btn_login_image, command=self.login, bg="#2C2F33", relief=tk.FLAT, padx=10, pady=5)
        self.btn_login.grid(row=3, columnspan=2)

        self.label_datetime = tk.Label(self.container, text="", bg="#2C2F33", fg="#FFFFFF", font="Tablón")
        self.label_datetime.grid(row=4, columnspan=2)

        self.update_datetime()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.db.check_credentials(username, password):
            self.master.withdraw()
            if username == "2":
                self.open_special_window(username)
            else:
                self.open_application_window(username)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def open_application_window(self, username):
        application_window = tk.Toplevel(self.master)
        application_window.title("Главное окно приложения")

        ApplicationWindow(application_window, self.db, username, self.master)

    def open_special_window(self, username):
        special_window = tk.Toplevel(self.master)
        special_window.title("Специальное окно для пользователя 2")

        special_window_instance = SpecialWindow(special_window, username, self, Database)

        tickets = self.db.get_all_tickets()
        special_window_instance.display_tickets(tickets)

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def show(self):
        self.master.deiconify()

def main():
    root = tk.Tk()
    root.configure(bg="#2C2F33")  # Темный фон
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
