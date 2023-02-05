'''
Requirements
1. Using two threads, put cars onto a shared queue, with one thread consuming
   the items from the queue and the other producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. Produce a Plot of car count vs queue size (okay to use q.size since this is not a
   condition statement).
   
Questions:
1. Do you need to use locks around accessing the queue object when using multiple threads? 
   Why or why not?
   > I had one created but no I did not 
   > Working on the code the only thing I had to do is have the second tread wait for a little bit
2. How would you define a semaphore in your own words?
   > It is a grate way to have the computer track what is going on in the code and for it 
   >
3. Read https://stackoverflow.com/questions/2407589/what-does-the-term-blocking-mean-in-programming.
   What does it mean that the "join" function is a blocking function? Why do we want to block?
   >
   >
   >
'''

from datetime import datetime
import time
import threading
import random
# DO NOT import queue

from plots import Plots

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

#########################
# NO GLOBAL VARIABLES!
#########################


class Car():
    """ This is the Car class that will be created by the factories """

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

        # Display the car that has just be created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, queue, cars, semaphoresmin, semaphoresmax, stats, lock):
        super().__init__()
        self.car_count = cars
        self.max = semaphoresmax
        self.min = semaphoresmin
        self.queue = queue
        self.stats = stats
        self.lock = lock
       

    def run(self):
        for _ in range(self.car_count):
            self.max.acquire()

            # Create a car
            car = Car()
            values = [car.make, car.model, car.year]

            # Place the car on the queue
            self.queue.put(values)

            # with self.lock:
                # self.stats += 1

            self.max.release()

        # Signal the dealers that there are no more cars
        if self.queue.size == 0:
                self.queue.put("No more cars!")
                self.max.release()

            

        # signal the dealer that there there are no more cars


class Dealership(threading.Thread):
    """ This is a dealership that receives cars """

    def __init__(self, queue, cars, semaphoresmin, semaphoresmax, stats, lock):
        super().__init__()
        self.car_count = cars
        self.max = semaphoresmax
        self.min = semaphoresmin
        self.queue = queue
        self.stats = stats
        self.lock = lock

    def run(self):
        while True:
            self.max.acquire()
            # Sell the car (take car from queue)
            print(self.queue.items)
            car = self.queue.get()
            if car == "No more cars!":
                break
            # with self.lock:
            #     self.stats += 1
            self.min.release()
            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def main():
    
    # Start a timer
    begin_time = time.perf_counter()

    # random amount of cars to produce
    CARS_TO_PRODUCE = random.randint(500, 600)

    # TODO Create semaphores
    semaphoresmax = threading.Semaphore(MAX_QUEUE_SIZE)
    semaphoresmin = threading.Semaphore(0)


    # TODO Create queue (ONLY use class QueueTwoFiftyOne)
    queue = QueueTwoFiftyOne()
    # TODO Create lock
    lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership,
    # the index of the list is the size of the queue. Update this list each time the
    # dealership receives a car (i.e., increment the integer at the index using the
    # queue size).
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one manufacturer
    manufacturer = Manufacturer(queue, CARS_TO_PRODUCE ,semaphoresmin, semaphoresmax, queue_stats, lock)
    
    # TODO create your one dealership
    dealership = Dealership(queue, CARS_TO_PRODUCE ,semaphoresmin, semaphoresmax, queue_stats, lock)
    # TODO Start manufacturer and dealership
    manufacturer.start()
    dealership.start()

    # TODO Wait for manufacturer and dealership to complete
    manufacturer.join()
    dealership.join()

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

    # Plot car count vs queue size
    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats,
             title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')
    


if __name__ == '__main__':
    main()
