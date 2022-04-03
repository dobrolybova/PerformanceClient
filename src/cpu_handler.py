import requests
import time
from http import HTTPStatus
from flask import Response
import psutil
import window_handler
import draw_handler
from log_handler import get_logger

time_interval = 1
logger = get_logger(__name__)


class CpuHandler:
    def __init__(self, running: bool) -> None:
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
            except requests.exceptions.RequestException:
                logger.critical("Connection error")
                time.sleep(time_interval)
                continue
            if not self.check_response_status(r):
                break
            logger.info(r.json())
            time.sleep(time_interval)

    def get_cpu(self):
        try:
            r = requests.get(
                f"http://localhost:5000/cpu?hash={self.user_hash}&start_time={self.start_time}&cur_time={time.time()}")
            if self.check_response_status(r):
                draw_handler.draw_data(r.json()['payload'])
        except requests.exceptions.RequestException:
            window_handler.draw_separate_window("Connection error")

    @staticmethod
    def check_response_status(response: Response) -> bool:
        if response.status_code != HTTPStatus.OK:
            window_handler.draw_separate_window(f"ERROR: {response.json()} ")
            return False
        return True
