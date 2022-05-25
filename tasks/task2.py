#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from threading import Thread, Lock
from math import sqrt
from queue import Queue

q = Queue()
lock = Lock()


def infinite_sum(x):
    lock.acquire()
    eps = 10 ** -7
    a = 1
    summa = 1
    i = 1
    prev = 0
    while abs(summa - prev) > eps:
        prev = summa
        numerator = 1
        denominator = 1
        for j in range(1, i + 1):
            if 2 * j - 3 > 0:
                numerator *= 2 * j - 3
            denominator *= 2 * j
        temp = (numerator / denominator) * x ** i
        if (-1) ** (i + 1) > 0:
            summa += temp
        else:
            summa -= temp
        i += 1
    q.put(summa)
    lock.release()


def checker(calc_result, n_result):
    print(f"Calculated sum: {calc_result}")
    print(f"Verification sum: {n_result}")


if __name__ == '__main__':
    checksum = sqrt(1 - 0.8)
    thread1 = Thread(target=infinite_sum, args=(-0.8, ))
    thread1.start()
    thread1 = Thread(target=checker, args=(q.get(), checksum))
    thread1.start()
