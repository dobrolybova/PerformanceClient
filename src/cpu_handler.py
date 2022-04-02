import requests
import time
from http import HTTPStatus
from flask import Response
import psutil
import window_handler

time_interval = 1


class CpuHandler:
    def __init__(self, running):
        self.running = running
        self.user_hash = None
        self.start_time = time.time()

    def post_cpu(self, user_hash: str) -> None:
        self.user_hash = user_hash
        while self.running:
            cpu = psutil.cpu_percent()
            try:
                r = requests.post("http://localhost:5000/cpu",
                                  json={"hash": user_hash, "cpu": cpu, "time": time.time()})
            except Exception:
                print("Connection error")
                time.sleep(time_interval)
                continue
            if not self.check_response_status(r):
                break
            print(r.json())
            time.sleep(time_interval)

    @staticmethod
    def check_response_status(response: Response) -> bool:
        if response.status_code != HTTPStatus.OK:
            window_handler.draw_separate_window(f"ERROR: {response.json()} ")
            return False
        return True
