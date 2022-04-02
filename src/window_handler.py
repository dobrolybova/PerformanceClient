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


class CredentialsWindowHandler:
    def __init__(self, window_title: str, authentication_handler: AuthenticationHandler):
        self.window = Tk()
        self.window.title(window_title)
        self.window.geometry('550x200')
        self.user_label = Label(self.window, text="user name")
        self.user_label.grid(column=0, row=0)
        self.user_entry = Entry(self.window, width=10)
        self.user_entry.grid(column=1, row=0)
        self.passwd_label = Label(self.window, text="user password")
        self.passwd_label.grid(column=2, row=0)
        self.passwd_entry = Entry(self.window, width=10, show="*")
        self.passwd_entry.grid(column=3, row=0)
        self.register_button = Button(self.window, text="register", command=self.clicked_register)
        self.register_button.grid(column=4, row=0)
        self.login_button = Button(self.window, text="login", command=self.clicked_login)
        self.login_button.grid(column=5, row=0)
        self.user_auth_handler = authentication_handler
        self.window.mainloop()

    def clicked_register(self) -> None:
        self.user_auth_handler.register(self.user_entry.get(), self.passwd_entry.get())
        if self.user_auth_handler.get_hash():
            self.window.destroy()

    def clicked_login(self) -> None:
        self.user_auth_handler.login(self.user_entry.get(), self.passwd_entry.get())
        if self.user_auth_handler.get_hash():
            self.window.destroy()


class GetCpuWindowHandler:
    def __init__(self, window_title: str, cpu_handler: CpuHandler):
        self.window = Tk()
        self.window.title(window_title)
        self.window.geometry('550x200')
        self.get_cpu_button = Button(self.window, text="get cpu", command=self.clicked_get_cpu)
        self.get_cpu_button.grid(column=1, row=0)
        self.cpu_handler = cpu_handler
        self.window.mainloop()

    def clicked_get_cpu(self):
        try:
            r = requests.get(
                f"http://localhost:5000/cpu?hash={self.cpu_handler.user_hash}&start_time={self.cpu_handler.start_time}&cur_time={time.time()}")
            self.cpu_handler.check_response_status(r)
            draw_handler.draw_data(r.json()['payload'])
        except Exception:
            draw_separate_window("Connection error")



