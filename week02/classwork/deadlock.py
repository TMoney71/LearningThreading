from threading import Lock, Thread
import threading


def transfer(lock1: Lock, lock2: Lock):
    print(f'{threading.current_thread().name}, locking account one\n', end="")
    lock1.acquire()

    print(f'{threading.current_thread().name}, locking account two\n', end="")
    lock2.acquire()

    print(f'{threading.current_thread().name}, transferring money\n', end="")

    print(f'{threading.current_thread().name}, release account one\n', end="")
    lock1.release()

    print(f'{threading.current_thread().name}, release account two\n', end="")
    lock2.release()


def transfer_do(lock1, lock2):

    while True:

        # send money from first account to second
        transfer(lock1, lock2)

        # send money from second account to first
        transfer(lock2, lock1)


if __name__ == '__main__':

    account_one_lock = Lock()
    account_two_lock = Lock()

    # TODO - create 2 threads to transfer money fro account one to account two.
    for x in range(2):
        t = Thread(target=transfer_do, args=(
            account_one_lock, account_two_lock))
        t.start()
