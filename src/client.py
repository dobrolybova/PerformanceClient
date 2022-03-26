import requests
import time
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
from http import HTTPStatus
from threading import Thread
import getpass

time_interval = 1
start_time = time.time()
running = True


def check_response_status(response):
    if response.status_code != HTTPStatus.OK:
        print(f"ERROR: {response.json()} ")
        exit(2)


def read_command_line_args():
    parser = argparse.ArgumentParser(description='Help.')
    parser.add_argument('--user', "-u", type=str, action='store', help='user')
    return parser.parse_args()


def register(user_name, user_passwd):
    r = requests.post("http://localhost:5000/register", json={"user": user_name, "passwd": user_passwd})
    check_response_status(r)
    return r.json()['hash']


def login(user_name, user_passwd):
    r = requests.post("http://localhost:5000/login", json={"user": user_name, "passwd": user_passwd})
    check_response_status(r)
    return r.json()['hash']


def post_cpu(user_hash):
    while running:
        cpu = psutil.cpu_percent()
        try:
            r = requests.post("http://localhost:5000/cpu", json={"hash": user_hash, "cpu": cpu, "time": time.time()})
        except Exception:
            print("Connection error")
            time.sleep(time_interval)
            continue
        check_response_status(r)
        print(r.json())
        time.sleep(time_interval)


def draw_data(data_list):
    y = data_list[0]
    x = [datetime.utcfromtimestamp(i).strftime('%H:%M:%S') for i in data_list[1]]
    print(x)
    print(y)
    plt.plot(x, y)
    plt.title('CPU CHART')
    plt.xlabel('TIMESTAMP')
    plt.ylabel('CPU VALUE')
    plt.show()


def get_cpu(user_hash):
    while running:
        input("Press Enter to get cpu data\n")
        try:
            r = requests.get(f"http://localhost:5000/cpu?hash={user_hash}&start_time={start_time}&cur_time={time.time()}")
        except Exception:
            print("Connection error")
            time.sleep(time_interval)
            continue
        check_response_status(r)
        print(r.json())
        #draw_data(r.json()['payload'])


def start_threads(user_hash):
    post_thread = Thread(target=post_cpu, args=(user_hash,))
    post_thread.start()
    get_thread = Thread(target=get_cpu, args=(user_hash,))
    get_thread.start()
    return post_thread, get_thread


def main():
    global running
    args = read_command_line_args()
    args.passwd = getpass.getpass()
    user_hash = register(args.user, args.passwd)
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
