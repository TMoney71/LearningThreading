import queue

q = queue.Queue()

q.put('House')
q.put('tree')
q.put('Farm')
q.put('truck')

item = q.get()
print(f'{item=}')
print(f'Size of queue = {q.qsize()}')

item = q.get()
print(f'{item=}')
print(f'Size of queue = {q.qsize()}')

item = q.get()
print(f'{item=}')
print(f'Size of queue = {q.qsize()}')

item = q.get()
print(f'{item=}')
print(f'eeeee Size of queue = {q.qsize()}')

item = q.get()
print(f'{item=}')
print(f'Size of queue = {q.qsize()}')