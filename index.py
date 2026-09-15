import threading
import time


def cpu_intensive():
    total = 0
    for i in range(50_000_000):
        total += i * i
    return total


# 多线程 vs 单线程 —— 多线程不会更快！
t1 = threading.Thread(target=cpu_intensive)
t2 = threading.Thread(target=cpu_intensive)

start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
print(f"多线程: {time.time() - start:.2f}s")

start = time.time()
cpu_intensive()
cpu_intensive()
print(f"单线程: {time.time() - start:.2f}s")
