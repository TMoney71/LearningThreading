'''
Requirements
1. Write a multithreaded program that counts the number of prime numbers 
   between 10,000,000,000 and 10,000,110,003.
2. The program should be able to use a variable amount of threads.
3. Each thread should look over an approximately equal number of numbers.
   This means that you need to divise an algorithm that can divide up the
   110,003 numbers "fairly" based on a variable number of threads. 
   
Psuedocode: 
1. Create variable for the start number (10_000_000_000)
2. Create variable for range of numbers to examine (110_003)
3. Create variable for number of threads (start with 1 to get your program running,
   then increase to 5, then 10).
4. Determine an algorithm to partition the 110,003 numbers based on x
    the number of threads. Each thread should have approx. the same amount
    of numbers to examine. For example, if the number of threads is
    5, then the first 4 threads will examine 22,003 numbers, and the
    last thread will examine 22,003 numbers. Determine the start and
    end values of each partition.
5. Use these start and end values as arguments to a function.
6. Use a thread to call this function.
7. Create a function that loops from a start and end value, and checks
   if the value is prime using the isPrime function. Use the globals
   to keep track of the total numbers examined and the number of primes
   found. 

Questions:
1. Time to run using 1 thread = 51.83
2. Time to run using 5 threads = 47.70
3. Time to run using 10 threads = 47.66
4. Based on your study of the GIL (see https://realpython.com/python-gil), 
   what conclusions can you draw about the similarity of the times (short answer)?
   > That for this amount of numbers you dont need many threads to get the most efficent
   > The more threads that you have the more likely it is to go faster it may not be by much but it does go faster
5. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
   >This is more cpu bound doing calulations
'''

from datetime import datetime, timedelta
import math
import threading
import time

# Global count of the number of primes found
prime_count = 0

# Global count of the numbers examined
numbers_processed = 0



def is_prime(n: int):
    global numbers_processed
    # global prime_count

    numbers_processed += 1 
    """
    Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test

    Parameters
    ----------
    ``n`` : int
        Number to determine if prime

    Returns
    -------
    bool
        True if ``n`` is prime.
    """

    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6  
    return True
    
def run(start, end):
    global prime_count
    for i in range(start, end):
        if is_prime(i):
            prime_count += 1
            print(i, end=', ', flush=True)


if __name__ == '__main__':
    # Start a timer
    begin_time = time.perf_counter()

    # starting the counting at 10 billion
    startingNumber = 10000000000
    # the numbers that we are going too
    range_of_numbers = 110003
    # The number of threads we want to us in this program
    numberofthreads = 10
    # a list so we can add each thread too and their actions to be able to run it out of the list
    groups = []
    #This gives the range of how many numbers fit into on thread so it is even
    thread_range = range_of_numbers // numberofthreads
    # This is so we can see if there is a remainder of numbers if the # of threads do not go into the range evenly
    remainder = range_of_numbers % numberofthreads

    for i in range(numberofthreads):
        # Becaue python retunds indexes as 0, 1, 2 we need to find the last one and add the remainder to it for example in this case with 5 or 10
        # we have a remander of 3. That is why we look for this.
        if i is numberofthreads - 1 :
            # We know that 1 can go into everything and also matches our if statement before we know that there is no remainder so we need to run it 
            # where 1 runs as normal
            if numberofthreads == 1:
                start_thread = startingNumber + (thread_range * i)
                # print(start_thread)
                thread_end = start_thread + thread_range
                # print(thread_end)
                t = threading.Thread(target=run, args=(start_thread, thread_end))
                groups.append(t)
            # This is for the 5 - 10 where we know that we have 3 left over with the example that we have. So we need to add 3 to the last thread that runs
            # This will work for other examples where if we changed the number of threads it will take the last one and add the remainder so we can check all
            # the number given to us
            else:
                start_thread = startingNumber + (thread_range * i)
                
                thread_end = start_thread + (thread_range + remainder)
                # print(thread_end)
                t = threading.Thread(target=run, args=(start_thread, thread_end))
                groups.append(t)
        # This is for every other number that is not effected by the other clauses where you can run it in the range that we got
        else:
            start_thread = startingNumber + (thread_range * i)
            # print(start_thread)
            thread_end = start_thread + thread_range
            # print(thread_end)
            t = threading.Thread(target=run, args=(start_thread, thread_end))
            groups.append(t)

            


    

    # for i in range(numberofthreads): 
    #     groups.append(int(range_of_numbers/numberofthreads))

    # finalnum = groups.pop(0)
    # remainder = range_of_numbers%numberofthreads
    # finalnum = finalnum + remainder
    # groups.append(finalnum)
    # print(groups)

    # rangeofnumbers = [i+startingNumber for i in groups]
    # print(rangeofnumbers)

    




    # threads = [threading.Thread(target=is_prime, args=(,)) for _ in numberofthreads
    
    # Starting the threads from the list of threads that we had prior
    for t in groups:
        t.start()
    # Joining the groups to end them from that same list
    for t in groups:
        t.join()


    
    # Use the below code to check and print your results
    assert numbers_processed == 110_003, f"Should check exactly 110,003 numbers but checked {numbers_processed}"
    assert prime_count == 4764, f"Should find exactly 4764 primes but found {prime_count}"

    print(f'Numbers processed = {numbers_processed}')
    print(f'Primes found = {prime_count}')
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')
