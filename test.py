import numpy as np
import random


def bar():
    num = 0
    while True:
        yield num
        num += 1
        if num > 9:
            break


def foo():
    data = random.sample(range(0, 10), 5)
    print(data)
    for item in data:
        yield item


for i in foo():
    print(i)

for i in bar():
    print(i)
