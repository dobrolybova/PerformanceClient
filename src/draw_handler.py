import matplotlib.pyplot as plt
from typing import List, Dict
from datetime import datetime


def draw_data(data_list: List[Dict]) -> None:
    #{'cpu': cpu, 'timestamp': time}
    y = [i.get('cpu') for i in data_list]
    x = [datetime.utcfromtimestamp(i.get('timestamp')).strftime('%H:%M:%S') for i in data_list]
    #y = data_list[0]
    #x = [datetime.utcfromtimestamp(i).strftime('%H:%M:%S') for i in data_list[1]]
    print(x)
    print(y)
    plt.plot(x, y)
    plt.title('CPU CHART')
    plt.xlabel('TIMESTAMP')
    plt.ylabel('CPU VALUE')
    plt.show()
