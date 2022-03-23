import requests
import time
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
from http import HTTPStatus
from threading import Thread

time_interval = 1
start_time = time.time()
running = True


def check_response_status(response):
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        reason = response.json()["reason"]
        print(f"ERROR: {reason} ")
        exit(2)


def read_command_line_args():
    parser = argparse.ArgumentParser(description='Help.')
    parser.add_argument('--user', "-u", type=str, action='store', help='user')
    parser.add_argument('--passwd', "-p", type=str, action='store', help='passwd')
    return parser.parse_args()


def login(user_name, user_passwd):
    r = requests.post("http://localhost:5000/login", json={"user": user_name, "passwd": user_passwd})
    check_response_status(r)
    return r.json()['hash']


def post_cpu(user_hash):
    while running:
        cpu = psutil.cpu_percent()
        r = requests.post("http://localhost:5000/cpu", json={"hash": user_hash, "cpu": cpu, "time": time.time()})
        check_response_status(r)
        print(r.json())
        time.sleep(time_interval)


def draw_data(data_list):
    y = [i[0] for i in data_list]
    x = [datetime.utcfromtimestamp(i[1]).strftime('%H:%M:%S') for i in data_list]
    print(x)
    print(y)
    plt.plot(x, y)
    plt.title('CPU CHART')
    plt.xlabel('TIMESTAMP')
    plt.ylabel('CPU VALUE')
    plt.show()


def get_cpu(user_hash):
    while running:
        input("Press Enter to get cpu data")
        r = requests.get(f"http://localhost:5000/cpu?hash={user_hash}&start_time={start_time}&cur_time={time.time()}")
        check_response_status(r)
        print(r.json())
        draw_data(r.json()['get_data'])


def start_threads(user_hash):
    post_thread = Thread(target=post_cpu, args=(user_hash,))
    post_thread.start()
    get_thread = Thread(target=get_cpu, args=(user_hash,))
    get_thread.start()
    return post_thread, get_thread


def main():
    global running
    args = read_command_line_args()
    user_hash = login(args.user, args.passwd)
    try:
        post_thread, get_thread = start_threads(user_hash)
    except KeyboardInterrupt:
        running = False
        post_thread.join()
        get_thread.join()
        exit(2)


if __name__ == '__main__':
    main()
