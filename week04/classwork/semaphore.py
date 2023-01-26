import threading

DISPLAY_THREADS = 3

def display(sem: threading.Semaphore, name):
    
    print(f'Thread-{name}: value before acquire = {sem._value}\n', end="")
    sem.acquire()
    print(f'Thread-{name}: value after acquire = {sem._value}\n', end="")
    
def increment(sem: threading.Semaphore):
    
    for _ in range(DISPLAY_THREADS):
        sem.release()

def main():
    
    sem = threading.Semaphore(0)
    
    l = []
    l.pop()
    
    threads = [threading.Thread(target=display, args=(sem, f'{i}')) for i in range(DISPLAY_THREADS)]
    threads.append(threading.Thread(target=increment, args=(sem,)))
    
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()