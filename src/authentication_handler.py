import requests
from http import HTTPStatus
from flask import Response
import window_handler


class AuthenticationHandler:
    def __init__(self):
        self.hash = None

    def register(self, user_name: str, user_passwd: str) -> None:
        if self.validate_credentials(user_name, user_passwd):
            r = requests.post("http://localhost:5000/register", json={"user": user_name, "passwd": user_passwd})
            if self.check_response_status(r):
                self.hash = r.json()['hash']

    def login(self, user_name: str, user_passwd: str) -> None:
        if self.validate_credentials(user_name, user_passwd):
            r = requests.post("http://localhost:5000/login", json={"user":  user_name, "passwd": user_passwd})
            if self.check_response_status(r):
                self.hash = r.json()['hash']

    def get_hash(self) -> str:
        return self.hash

    @staticmethod
    def validate_credentials(user_name: str, user_passwd: str) -> bool:
        if user_name != "" and user_passwd != "":
            return True
        else:
            window_handler.draw_separate_window("No user name or password")
            return False

    @staticmethod
    def check_response_status(response: Response) -> bool:
        if response.status_code != HTTPStatus.OK:
            window_handler.draw_separate_window(f"ERROR: {response.json()} ")
            return False
        return True

