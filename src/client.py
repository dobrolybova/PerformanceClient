from window_handler import credentials_window_handler, get_cpu_window_handler
from threading import Thread
from authentication_handler import AuthenticationHandler
from cpu_handler import CpuHandler
from logging import INFO, DEBUG, CRITICAL,  WARNING
from log_handler import make_logs_dir, set_imported_modules_log_level, set_log_level

file_name = make_logs_dir("logs")
set_log_level(file_name, INFO)
set_imported_modules_log_level(WARNING)


def start_threads(user_hash: str, cpu_h: CpuHandler):
    post_thread = Thread(target=cpu_h.post_cpu, args=(user_hash,))
    post_thread.start()
    return post_thread


def main():
    a_h = AuthenticationHandler()
    credentials_window_handler("Enter user and password", a_h)
    cpu_h = CpuHandler(True)
    post_thread = None
    try:
        post_thread = start_threads(a_h.get_hash(), cpu_h)
    except KeyboardInterrupt:
        cpu_h.running = False
        if not post_thread:
            post_thread.join()
        exit(2)
    get_cpu_window_handler("Get cpu", cpu_h)


if __name__ == '__main__':
    main()
