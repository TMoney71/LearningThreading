import threading
'''
Requirements:Create a class that extends the 'threading.Thread'
1.  class (see https://stackoverflow.com/questions/15526858/how-to-extend-a-class-in-python). This means that the class IS a thread. 
   Any objects instantiated using this class ARE threads.
2. Instantiate this thread class that computes the sum of all numbers 
   between one and that number (exclusive)

Psuedocode:
1. In your class, write a constructor (in python a constructor is __init__) and allow a number
   to be passed in as a parameter.
2. The constructor should call the parent class's constructor:
   threading.Thread.__init__(self)
3. Create a local sum variable in your constructor.
4. A thread must have a run function, so create a run function that sums from one to the 
   passed in number (inclusive).
5. In the run function, set the sum on self.
6. In main, instantiate your thread class with the a value of 10.
7. Start the thread.
8. Wait for the thread to finish.
9. Assert that thread object's sum attribute is equal to the appropriate value (see main).
10. Repeat steps 7 through 10 using a value of 13.
11. Repeat steps 7 through 10 using a value of 17.

Things to consider:
a. How do you instantiate a class and pass in arguments (see https://realpython.com/lessons/instantiating-classes/)?
b. How do you start a thread object (see this week's reading)?
c. How will you wait until the thread is done (see this week's reading)?
d. How do you get the value an object's attribute (see https://datagy.io/python-print-objects-attributes/)?
'''
######################
# DO NOT USE GLOBALS #
######################

class SummingNumbers(threading.Thread):
    '''Sums numbers'''
    def __init__(self, number):
        threading.Thread.__init__(self)
        self.sum = 0
        self.number = number

    def run(self):
        for x in range(self.number):
            self.sum = self.sum + x
            #print(f'{self.sum=}')
            
def main():
    
    t1 = SummingNumbers(10)
    t2 = SummingNumbers(13)
    t3 = SummingNumbers(17)
    
    t1.start()
    t2.start()
    t3.start()
    
    t1.join()
    t2.join()
    t3.join()
    
    # Instantiate your thread class and pass in 10.
    # Test (assert) if its sum attribute is equal to 45.
    # Note: do no use 'yourThread' for the name of your thread object
    assert t1.sum == 45, f'The sum should equal 45 but instead was {t1.sum}'
    
    # Repeat, passing in 13
    assert t2.sum == 78, f'The sum should equal 78 but instead was {t2.sum}'
    
    # Repeat, passing in 17
    assert t3.sum == 136, f'The sum should equal 136 but instead was {t3.sum}'

if __name__ == '__main__':
    main()
    assert threading.active_count() == 1
    print("DONE")
