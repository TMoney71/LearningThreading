'''
Requirements
1. Using multiple threads, put cars onto a shared queue, with one or more thread consuming
   the items from the queue and one or more thread producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. Produce a Plot of car count vs queue size (okay to use q.size since this is not a
   condition statement).
5. The number of cars produced by the manufacturer must equal the number of cars bought by the 
   dealership. Use necessary data objects (e.g., lists) to prove this. There is an assert in 
   main that must be used.
   
Questions:
1. How would you define a barrier in your own words?
   > It is like a gate where you can only allow this many people in no more no less
   >
2. Why is a barrier necessary in this assignment?
   >You cant send the all finished before each thread is done you have to wait for them all to be done 
   >or the program will end before it is supposed to
'''

from datetime import datetime, timedelta
import time
import threading
import random

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!


class Car():
    """ This is the Car class that will be created by the manufacturers """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru',
                 'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus',
                 'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE', 'Super', 'Tall', 'Flat', 'Middle', 'Round',
                  'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                  'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, id, queue, semaphoresmin: threading.Semaphore, semaphoresmax: threading.Semaphore, stats, dealer_count, lock, barrier: threading.Barrier):
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        super().__init__()
        self.id = id
        self.max = semaphoresmax
        self.min = semaphoresmin
        self.queue = queue
        self.stats = stats
        self.dealer = dealer_count
        self.lock = lock
        self.barrier = barrier
       

    def run(self):
        for _ in range(self.cars_to_produce):
            self.min.acquire()

            # Create a car
            car = Car()
            # values = [car.make, car.model, car.year]

            # Place the car on the queue
            self.queue.put(car)
            # print(self.queue)

            with self.lock:
                self.stats[self.id] += 1

            self.max.release()
        # Wait until all factories are finished producing cars
        self.barrier.wait()

        # Signal the dealers that there are no more cars
        if self.id == 0:
            for _ in range(self.dealer):
                self.queue.put("No more cars!")
                self.max.release()


class Dealership(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, id, queue, semaphoresmin:threading.Semaphore, semaphoresmax:threading.Semaphore, stats, lock):
        super().__init__()
        self.id = id
        self.max = semaphoresmax
        self.min = semaphoresmin
        self.queue = queue
        self.stats = stats
        self.lock = lock

    def run(self):
        while True:
            self.max.acquire()
            # Sell the car (take car from queue)
            # print(self.queue.items)
            car = self.queue.get()
            if car == "No more cars!":
                break

            with self.lock:
                self.stats[self.id] += 1
            self.min.release()
            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def run_production(manufacturer_count, dealer_count):
    """ This function will do a production run with the number of
        manufacturers and dealerships passed in as arguments.
    """

    # Start a timer
    begin_time = time.perf_counter()

    # TODO Create semaphore(s)
    semaphoresmax = threading.Semaphore(0)
    semaphoresmin = threading.Semaphore(MAX_QUEUE_SIZE)

    # TODO Create queue
    queue = QueueTwoFiftyOne()
    # TODO Create lock(s)
    lock = threading.Lock()
    # TODO Create barrier(s)
    barrier = threading.Barrier(manufacturer_count)


    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)
    manufacturer_stats = list([0] * manufacturer_count)

    # TODO create your manufacturers, each manufacturer will create CARS_TO_CREATE_PER_MANUFACTURER
    manufacturer = [Manufacturer(i, queue, semaphoresmin, semaphoresmax, manufacturer_stats, dealer_count, lock, barrier) for i in range(manufacturer_count)]

    # TODO create your dealerships
    dealers = [Dealership(i, queue, semaphoresmin, semaphoresmax, dealer_stats, lock) for i in range(dealer_count)]
    # TODO Start all dealerships
    for i in range(dealer_count):
        dealers[i].start()
    
    time.sleep(1)
    # TODO Start all manufacturers
    for i in range(manufacturer_count):
        manufacturer[i].start()

    # TODO Wait for manufacturers and dealerships to complete
    time.sleep(1)
    for i in range(manufacturer_count):
        manufacturer[i].join()

    for i in range(dealer_count):
        dealers[i].join()

    run_time = time.perf_counter() - begin_time

    # This function must return the following - only change the variable names, if necessary.
    # manufacturer_stats: is a list of the number of cars produced by each manufacturer,
    #                collect this information after the manufacturers are finished.
    return (run_time, queue.get_max_size(), dealer_stats, manufacturer_stats)


def main():
    """ Main function """

    # Use 1, 1 to get your code working like the previous assignment, then
    # try adding in different run amounts. You should be able to run the
    # full 7 run amounts.
    # runs = [(1, 1)]
    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for manufacturers, dealerships in runs:
        run_time, max_queue_size, dealer_stats, manufacturer_stats = run_production(
            manufacturers, dealerships)

        print(f'Manufacturers       : {manufacturers}')
        print(f'Dealerships         : {dealerships}')
        print(f'Run Time            : {run_time:.2f} sec')
        print(f'Max queue size      : {max_queue_size}')
        print(f'Manufacturer Stats  : {manufacturer_stats}')
        print(f'Dealer Stats        : {dealer_stats}')
        print('')

        # The number of cars produces needs to match the cars sold (this should pass)
        assert sum(dealer_stats) == sum(manufacturer_stats)


if __name__ == '__main__':
    main()
