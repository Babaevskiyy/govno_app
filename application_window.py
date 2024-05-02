import tkinter as tk
import datetime
from ticket_form import TicketForm
from ticket_edit_form import TicketEditForm
import statistics_window
from tkinter import ttk

class ApplicationWindow:
    def __init__(self, master, db, current_user, root, *args, **kwargs):
        self.master = master
        self.root = root  
        self.db = db
        self.current_user = current_user

        self.master.title("Главное окно приложения")
        self.master.configure(bg="#2C2F33")  

        self.main_frame = tk.Frame(master, bg="#2C2F33")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label_style = ttk.Style()
        self.label_style.configure("Dark.TLabel", foreground="#FFFFFF", background="#2C2F33", font="Tablón")

        self.button_style = ttk.Style()
        self.button_style.configure("Dark.TButton", foreground="#000000", background="#2C2F33", relief=tk.FLAT, padx=10, pady=5, font="Tablón")

        self.btn_logout = ttk.Button(self.main_frame, text="Выйти", style="Dark.TButton", command=self.logout)
        self.btn_logout.pack()

        self.btn_statistics = ttk.Button(self.main_frame, text="Статистика", command=self.open_statistics_window, style="Dark.TButton")
        self.btn_statistics.pack()

        self.btn_create_ticket = ttk.Button(self.main_frame, text="Создать заявку", command=self.create_ticket, style="Dark.TButton")
        self.btn_create_ticket.pack()

        self.search_frame = tk.Frame(self.main_frame, bg="#2C2F33") 
        self.search_frame.pack()

        self.search_label = ttk.Label(self.search_frame, text="Поиск:", style="Dark.TLabel")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame, relief=tk.FLAT, bg="#40444B", fg="#FFFFFF", insertbackground="#FFFFFF", font="Tablón")
        self.search_entry.pack(side=tk.LEFT)

        self.search_button = ttk.Button(self.search_frame, text="Найти", command=self.search_tickets, style="Dark.TButton")
        self.search_button.pack(side=tk.LEFT)

        self.ticket_canvas = tk.Canvas(self.main_frame, bg="#2C2F33")
        self.ticket_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.inner_frame = tk.Frame(self.ticket_canvas, bg="#2C2F33")
        self.inner_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.ticket_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.ticket_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.ticket_canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)
        self.inner_frame.bind("<Configure>", self.on_frame_configure)

        self.update_ticket_info()

    def on_frame_configure(self, event):
        self.ticket_canvas.configure(scrollregion=self.ticket_canvas.bbox("all"))

    def create_ticket(self):
        current_datetime = datetime.datetime.now()  
        latest_ticket = self.db.get_latest_ticket()
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Форма заявки")
        ticket_form = TicketForm(ticket_window, self.db, self, creation_time=current_datetime)
   
    def open_statistics_window(self):
        statistics_window.create_statistics_window(self.db)

    def edit_ticket(self, ticket_id):
        ticket = self.db.get_ticket_by_id(ticket_id)
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Редактировать заявку")
        ticket_edit_form = TicketEditForm(ticket_window, self.db, ticket_id, self)

    def delete_ticket(self, ticket_id):
        self.db.delete_ticket(ticket_id)
        self.update_ticket_info()

    def search_tickets(self):
        search_query = self.search_entry.get()
        if search_query:
            tickets = self.db.search_tickets(search_query)
            self.display_search_results(tickets)
        else:
            self.update_ticket_info()

    def display_search_results(self, tickets):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for ticket in tickets:
            ticket_info = f"Заявка #: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОптисание неисправности: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:  
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(self.inner_frame, text=ticket_info, bg="#2C2F33", fg="#FFFFFF", font="Tablón")
            label.pack()

            edit_button = tk.Button(self.inner_frame, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket(t), bg="#2C2F33", fg="#FFFFFF")
            edit_button.pack()

            delete_button = tk.Button(self.inner_frame, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t), bg="#2C2F33", fg="#FFFFFF")
            delete_button.pack()

        if tickets:
            self.label_ticket_info.config(text="Заявки")
        else:
            self.label_ticket_info.config(text="Нет созданных заявок")

    def update_ticket_info(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        tickets = self.db.get_all_tickets()
        for ticket in tickets:
            ticket_info = f"Заявка #: {ticket[1]}\nОборудование: {ticket[2]}\nОписание проблемы: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:  
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(self.inner_frame, text=ticket_info, bg="#2C2F33", fg="#FFFFFF", font="Tablón")
            label.pack()

            edit_button = tk.Button(self.inner_frame, text="Редактровать", command=lambda t=ticket[0]: self.edit_ticket(t), bg="#2C2F33", fg="#FFFFFF")
            edit_button.pack()

            delete_button = tk.Button(self.inner_frame, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t), bg="#2C2F33", fg="#FFFFFF")
            delete_button.pack()

        if tickets:
            self.label_ticket_info.config(text="Результаты поиска")
        else:
            self.label_ticket_info.config(text="Заявки не найдены")

    def logout(self):
        self.master.destroy()
        self.root.deiconify() 