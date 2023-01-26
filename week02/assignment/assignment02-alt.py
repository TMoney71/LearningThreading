'''
Requirements
1. Write a multithreaded program that counts the number of prime numbers 
   between 1,000,000 and 1,110,003.
2. The program will need to perform requirement #1 using first 1 thread, then 
   2 threads, then 3, all the way up to 30 threads. Each time it loops
   the number of threads should increase (you will not be manually changing
   the number of threads, the program needs to do this in a loop).
3. Each thread should look over an approximately equal range of numbers.
   This means that you need to devise an algorithm that can divide up the
   100,003 numbers "fairly" based on a the number of threads. 
4. Store the number of primes in a list (NOT global).
5. Print out the time it takes for each iteration (don't forget to reset
   your beginning time each time you loop using a new number of threads).
   
Psuedocode: 
1. Create variable for the start number (1_000_000).
2. Create variable for range of numbers to examine (110_003)
3. Create variable for number of maximum number of threads to create
   (NUMBER_THREADS).
4. Loop from 1 to NUMBER_THREADS.
5. Create a list of integers of a size equal to the number of threads
   (primes = [0] * thread_count).
6. Determine an algorithm to partition the 110,003 numbers based on 
    the number of threads. Each thread should have approx. the same amount
    of numbers to examine. For example, if the number of threads is
    5, then the first 4 threads will examine 22,000 numbers, and the
    last thread will examine 22,003 numbers. Determine the start and
    end values of each partition.
7. Use these start and end values as arguments to a function, as well as
   the primes list (from step #5).
8. Use a thread to call this function.
9. This new function (that is the target of your thread) should loop 
   from a start and end value, and check if the value is prime using 
   the isPrime function. Also pass in a thread index.
10. If the number is prime, then increment the appropriate integer
    in the shared list using the thread's index. So, for example, if 
    the function is running in thread 1, and a number is prime, then
    you would do this: primes[index] += 1 

Questions:
1. Time to run using 1 thread =
2. Time to run using 5 threads =
3. Time to run using 10 threads =
4. Based on your study of the GIL (see https://realpython.com/python-gil), 
   what conclusions can you draw about the similarity of the times (short answer)?
   >
   >
5. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
   >
'''

from datetime import datetime, timedelta
import math
import threading
import time

# Global count of the numbers examined
numbers_processed = 0

NUMBER_THREADS = 30 # might want to start with 1 to get things working

# Don't add a global for counting number of primes, use a list

def is_prime(n: int):
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

# TODO add function here

if __name__ == '__main__':
    # Start a timer
    begin_time = time.perf_counter()

    # TODO write code here
   
    # Use the below code to check and print your results
    prime_count = sum(primes) # where primes is your list
    assert numbers_processed == 110_003, f"Should check exactly 110,003 numbers but checked {numbers_processed}"
    assert prime_count == 7952, f"Should find exactly 7952 primes but found {prime_count}"

    print(f'Numbers processed = {numbers_processed}')
    print(f'Primes found = {prime_count}')
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')
