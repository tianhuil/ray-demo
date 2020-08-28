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

"""
Ray is about 3X faster.  Probably because there's relatively little data passing back and forth.

2020-08-28 19:25:26,892 INFO resource_spec.py:223 -- Starting Ray with 33.54 GiB memory available for workers and up to 16.78 GiB for objects. You can adjust these settings with ray.init(memory=<bytes>, object_store_memory=<bytes>).
2020-08-28 19:25:27,389 INFO services.py:1191 -- View the Ray dashboard at localhost:8266
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 1000/1000 [00:28<00:00, 34.79it/s]
No ray: 28.753611secs
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 1000/1000 [00:09<00:00, 105.82it/s]
With ray: 9.535182secs
"""