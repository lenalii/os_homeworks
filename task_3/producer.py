#!/usr/bin/python3

import random
import time
import sys

n = random.randint(120, 180)
operations = ['+', '-', '*', '/']
for i in range (n):
  x = random.randint(1, 9)
  y = random.randint(1, 9)
  operation = random.choice(operations)

  sys.stdout.write(f"{x} {operation} {y}\n")
  sys.stdout.flush()
  time.sleep(1)