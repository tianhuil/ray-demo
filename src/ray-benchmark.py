import ray
import numpy as np

from contextlib import contextmanager
import datetime
import sys

dim = 150
T = 1000


@contextmanager
def timer(msg, out=sys.stdout):
    start = datetime.datetime.now()
    yield
    end = datetime.datetime.now()
    out.write("{}: {}secs\n".format(msg, (end - start).total_seconds()))

def inverse(A):
    return np.linalg.inv(A)

def func():
    [inverse(np.eye(dim) + np.random.normal(size=[dim, dim]) / dim) for _ in range(T)]

def ray_func():
    ray.get([ray.remote(inverse).remote(np.eye(dim) + np.random.normal(size=[dim, dim]) / dim) for _ in range(T)])


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
Ray takes longer
2020-08-28 19:12:40,425 INFO resource_spec.py:223 -- Starting Ray with 33.59 GiB memory available for workers and up to 16.8 GiB for objects. You can adjust these settings with ray.init(memory=<bytes>, object_store_memory=<bytes>).
2020-08-28 19:12:40,913 INFO services.py:1191 -- View the Ray dashboard at localhost:8266
No ray: 2.414631secs
2020-08-28 19:12:44,711 WARNING import_thread.py:126 -- The remote function '__main__.inverse' has been exported 100 times. It's possible that this warning is accidental, but this may indicate that the same remote function is being defined repeatedly from within many tasks and exported to all of the workers. This can be a performance issue and can be resolved by defining the remote function on the driver instead. See https://github.com/ray-project/ray/issues/6240 for more discussion.
With ray: 3.353522secs
"""