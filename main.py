import tkinter as tk
from auth_window import AuthWindow
from tkinter import ttk

def main():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()  
    screen_height = root.winfo_screenheight() 
    root.geometry(f"{screen_width}x{screen_height}")
    root.iconbitmap("weed.ico")
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()