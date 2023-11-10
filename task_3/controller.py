#!/usr/bin/python3

import os
import signal
import sys

pipe1 = os.pipe()
pipe0 = os.pipe()
pipe2 = os.pipe()

p1 = os.fork()
if p1 == 0:
    os.close(pipe1[0])
    os.dup2(pipe1[1], sys.stdout.fileno())
    os.execl('producer', 'producer')

p2 = os.fork()
if p2 == 0:
    os.close(pipe0[1])
    os.dup2(pipe0[0], sys.stdin.fileno())
    os.close(pipe2[0])
    os.dup2(pipe2[1], sys.stdout.fileno())
    os.execl('/usr/bin/bc', 'bc')

os.close(pipe1[1])
os.close(pipe0[0])
os.close(pipe2[1])

produced_count = 0

def print_produced_count(signum, frame):
    global produced_count
    sys.stderr.write(f"Produced: {produced_count}\n")
    sys.stderr.flush()

signal.signal(signal.SIGUSR1, print_produced_count)
while True:
    data = os.read(pipe1[0], 1024)
    if not data:
        break

    os.write(pipe0[1], data)
    R = os.read(pipe2[0], 1024)
    E = data.decode().strip()
    R = R.decode().strip()

    produced_count += 1
    sys.stdout.write(f"{E} = {R}\n")
    sys.stdout.flush()

os.close(pipe1[0])
os.close(pipe0[1])
os.close(pipe2[0])

os.kill(p1, signal.SIGTERM)
os.kill(p2, signal.SIGTERM)
