"""
Course: CSE 251
Lesson Week: 05
File: team05.py
Author: Brother Comeau (modified by Brother Foushee)

Purpose: Team Activity

Instructions:

- See in Canvas

"""

import threading
import queue
import time
import requests
import json

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(q: queue.Queue):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        url = q.get()
        if url == None:
            break
        else:
            search = requests.get(url)
            search = search.json()
            for i in search:
                if i == 'characters':
                    characters = search.get(i)
                    print(characters)
            
        # TODO process the value retrieved from the queue

        # TODO make Internet call to get characters name and print it out




def file_reader(q: queue.Queue): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """
    with open('urls.txt') as f:
        for line in f:
            # url = {line}

            # print(line)
            
            q.put(line)
     
    q.put(None)     

    
    






def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()
    
    # TODO create queue (if you use the queue module, then you won't need semaphores/locks)
    q = queue.Queue()
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread needed to do their jobs
    fileReader = threading.Thread(target=file_reader, args=(q, ))
    retrieveThread = threading.Thread(target=retrieve_thread, args=(q, ))
    # TODO Get them going

    # TODO Wait for them to finish

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time to process all URLS = {total_time} sec')


if __name__ == '__main__':
    main()




