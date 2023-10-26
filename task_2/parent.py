#!/usr/bin/python3
import os
import random
import sys

n = int(sys.argv[1])

def fork_child():
    child = os.fork()
    if child > 0:
        print(f'Parent[{os.getpid()}]: I ran children process with PID {child}')
    else:
        rand_num = random.randint(5, 10)
        os.execl('./child.py', './child.py', str(rand_num))
    return child
count = n
while count >0:
    child=fork_child()
    if child > 0:
        count-=1
count = n
while count >0:
    child_pid, status = os.wait()
    if status != 0:
        child=fork_child()
    else:
        print(f'Parent[{os.getpid()}]: Child with PID {child_pid} terminated. Exit Status {status}.')
        count-=1
os._exit(os.EX_OK)