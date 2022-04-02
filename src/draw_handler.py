import matplotlib.pyplot as plt
from typing import List, Dict
from datetime import datetime


def draw_data(data_list: List[Dict]) -> None:
    y = [i.get('cpu') for i in data_list]
    x = [datetime.utcfromtimestamp(i.get('timestamp')).strftime('%H:%M:%S') for i in data_list]
    print(x)
    print(y)
    plt.plot(x, y)
    plt.title('CPU CHART')
    plt.xlabel('TIMESTAMP')
    plt.ylabel('CPU VALUE')
    plt.show()
