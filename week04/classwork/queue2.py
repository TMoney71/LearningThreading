import queue
import threading
import time


def read_thread(q: queue.Queue):
    
    while True:
        obj = q.get()
        
        if obj == None:
            print("breaking")
            break
        
        print(f'GET: {obj}')
        time.sleep(0.1)


def write_thread(index, q: queue.Queue):
    
    for i in range(10):
        print(f'{threading.current_thread().name}: put {i} on queue\n', end="")
        q.put(i)
        time.sleep(0.1)
        
    q.put(None)
        

def main():
    q = queue.Queue()
    
    reader = threading.Thread(target=read_thread, args=(q,))
    reader.start()

    threads = []
    for i in range(1):
        t = threading.Thread(target=write_thread, args=(i, q))
        t.start()
        threads.append(t)
    
    reader.join()
    for t in threads:
        t.join()
    
    







if __name__ == '__main__':
    main()