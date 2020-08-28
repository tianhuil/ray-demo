import ray
import numpy as np
from tqdm import tqdm

from contextlib import contextmanager
import datetime
import sys

from util import timer

N = 150
M = 20
T = 1000

class Inverter:
    def __init__(self):
        self.A = np.eye(N)
        self.A_inv = np.eye(N)

    def increment(self, x: np.array):
        self.A += np.outer(x, x)

    def inverse(self):
        self.A_inv = np.linalg.inv(self.A)


def func():
    invs = [Inverter() for _ in range(20)]
    for t in tqdm(range(T)):
        for inv in invs:
            inv.increment(np.random.normal(size=N) / N)
            inv.inverse()

def ray_func():
    invs = [ray.remote(Inverter).remote() for _ in range(20)]
    for t in tqdm(range(T)):
        for inv in invs:
            inv.increment.remote(np.random.normal(size=N) / N)
            inv.inverse.remote()

if __name__ == '__main__':
    ray.init()
    try:
        with timer('No ray'):
            func()

        with timer('With ray'):
            ray_func()
    finally:
        ray.shutdown()
