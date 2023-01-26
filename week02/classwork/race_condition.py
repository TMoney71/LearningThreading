import threading
import time
import random

global_counter = 0

def increase(number: int, lock: threading.Lock):
    global global_counter
    
    #print(f'BEFORE memory address of counter =       {id(global_counter)}')
    local_counter = global_counter
    #print(f'BEFORE memory address of local_counter = {id(local_counter)}')
    
    lock.acquire()
    local_counter += number
    
    # this represents a function doing some work/task
    time.sleep(random.uniform(0.1, 1))
    
    print(f'{threading.current_thread().name}: local_counter = {local_counter}\n', end="")
    
    #print(f'AFTER memory address of counter =       {id(global_counter)}')
    #print(f'AFTER memory address of local_counter = {id(local_counter)}')
    
    global_counter = local_counter
    print(f'{threading.current_thread().name}: global_counter = {global_counter}\n', end="")
    lock.release()


def main():
    
    lock = threading.Lock()
    t1 = threading.Thread(target=increase, args=(10, lock))
    t1.start()
    
    t2 = threading.Thread(target=increase, args=(20, lock))
    t2.start()
    
    # do other stuff
    t1.join()
    t2.join()
    
    print(f'INSIDE MAIN: global_counter = {global_counter}')





if __name__ == '__main__':
    main()