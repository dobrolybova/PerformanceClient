from tkinter import *
from authentication_handler import AuthenticationHandler
from cpu_handler import CpuHandler
import requests
import time
import draw_handler


def draw_separate_window(error_text: str) -> None:
    window = Tk()
    window.title("error window")
    label = Label(window, text=error_text)
    label.grid(column=1, row=0)
    window.mainloop()


def credentials_window_handler(window_title: str, authentication_handler: AuthenticationHandler):
    window = Tk()
    window.title(window_title)
    window.geometry('550x200')
    user_label = Label(window, text="user name")
    user_label.grid(column=0, row=0)
    user_entry = Entry(window, width=10)
    user_entry.grid(column=1, row=0)
    passwd_label = Label(window, text="user password")
    passwd_label.grid(column=2, row=0)
    passwd_entry = Entry(window, width=10, show="*")
    passwd_entry.grid(column=3, row=0)
    register_button = Button(window, text="register",
                             command=lambda: clicked_register(authentication_handler, window, user_entry, passwd_entry))
    register_button.grid(column=4, row=0)
    login_button = Button(window, text="login", command=lambda: clicked_login(authentication_handler, window, user_entry, passwd_entry))
    login_button.grid(column=5, row=0)
    window.mainloop()


def clicked_register(authentication_handler: AuthenticationHandler, window: Tk, user_entry: Entry, passwd_entry: Entry) -> None:
    authentication_handler.register(user_entry.get(), passwd_entry.get())
    if authentication_handler.get_hash():
        try:
            window.destroy()
        except TclError:
            pass


def clicked_login(authentication_handler: AuthenticationHandler, window: Tk, user_entry: Entry, passwd_entry: Entry) -> None:
    authentication_handler.login(user_entry.get(), passwd_entry.get())
    if authentication_handler.get_hash():
        try:
            window.destroy()
        except TclError:
            pass


def get_cpu_window_handler(window_title: str, cpu_handler: CpuHandler):
    window = Tk()
    window.title(window_title)
    window.geometry('550x200')
    get_cpu_button = Button(window, text="get cpu", command=lambda: clicked_get_cpu(cpu_handler))
    get_cpu_button.grid(column=1, row=0)
    window.mainloop()


def clicked_get_cpu(cpu_handler: CpuHandler):
    cpu_handler.get_cpu()

