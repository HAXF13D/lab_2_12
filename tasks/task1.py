#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from threading import Thread
from time import time
from queue import Queue


q = Queue()


def determinant(matrix, number):
    if len(matrix) == 1:
        return matrix[0][0]
    else:
        n = len(matrix)
        summa = 0
        for i in range(n):
            minor = []
            for x in range(n):
                temporary = []
                for y in range(n):
                    if x != i and y != 0:
                        temporary.append(matrix[x][y])
                if len(temporary) == n - 1:
                    minor.append(temporary)
            if i % 2 == 0:
                summa += matrix[i][0] * determinant(minor, -1)
            else:
                summa -= matrix[i][0] * determinant(minor, -1)
        if number != -1:
            q.put_nowait((number, summa))
        return float(summa)


def parallel(matrix):
    temp = []
    threads = []
    for i, elem in enumerate(matrix):
        temp.append(matrix[i][0])
    matrices = []
    n = len(matrix)
    for i in range(n):
        minor = []
        for x in range(n):
            temporary = []
            for y in range(n):
                if x != i and y != 0:
                    temporary.append(matrix[x][y])
            if len(temporary) == n - 1:
                minor.append(temporary)
        matrices.append(minor)
    for i, mat in enumerate(matrices):
        th = Thread(
            target=determinant,
            args=(mat, i,),
        )
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    answer = 0

    while not q.empty():
        i, det = q.get()
        if i % 2 == 0:
            answer += temp[i] * det
        else:
            answer -= temp[i] * det

    return answer


if __name__ == '__main__':
    data = np.matrix(np.random.randint(-9, 9, (9, 9)))
    data = data.tolist()
    start = time()
    print(parallel(data))
    time_par = time() - start
    print('Вычисление определителя заняло: {:.3f} секунд'
          .format(time_par)
          )
