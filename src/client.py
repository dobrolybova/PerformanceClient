from window_handler import CredentialsWindowHandler
from threading import Thread
from authentication_handler import AuthenticationHandler
from cpu_handler import CpuHandler


def start_threads(user_hash: str, cpu_h: CpuHandler):
    post_thread = Thread(target=cpu_h.post_cpu, args=(user_hash,))
    post_thread.start()
    get_thread = Thread(target=cpu_h.get_cpu, args=(user_hash,))
    get_thread.start()
    return post_thread, get_thread


def main():
    a_h = AuthenticationHandler()
    CredentialsWindowHandler("Enter user and password", a_h)
    cpu_h = CpuHandler(True)
    post_thread = None
    get_thread = None
    try:
        post_thread, get_thread = start_threads(a_h.get_hash(), cpu_h)
    except KeyboardInterrupt:
        cpu_h.running = False
        if not post_thread:
            post_thread.join()
        if not get_thread:
            get_thread.join()
        exit(2)


if __name__ == '__main__':
    main()
