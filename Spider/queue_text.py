import multiprocessing
import time
from queue import Queue

def write_queue(queue):
    # 循环写入数据
    for i in range(10):
        if queue.full():
            print("队列已满!")
            break
        # 向队列中放入消息
        queue.put(i)
        print(i)
        time.sleep(0.5)


def read_queue(queue):
    # 循环读取队列消息
    while True:
        # 队列为空，停止读取
        if queue.empty():
            print("---队列已空---")
            break

        # 读取消息并输出
        result = queue.get()
        print(result)


if __name__ == '__main__':
    queue = Queue()
    write_queue(queue)
    read_queue(queue)
