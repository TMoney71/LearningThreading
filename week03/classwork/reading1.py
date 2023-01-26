import threading
import time
import random

THREADS = 30
ITEMS = 1000000

def thread_function(data):
    for i in range(ITEMS):
        data[0] = data[0] + 1

def main():
    data = [0]
    start_time = time.perf_counter()

    # Create threads
    threads = [threading.Thread(
        target=thread_function, args=(data, )) for _ in range(THREADS)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(
        f'All work completed: {data[0]:,} in {time.perf_counter() - start_time:.5f} seconds')


if __name__ == '__main__':
    main()
