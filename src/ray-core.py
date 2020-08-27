import ray
import time

@ray.remote
class Counter(object):
    def __init__(self):
        self.counter = 0

    def inc(self):
        self.counter += 1

    def get_counter(self):
        return self.counter


@ray.remote
def f(counter):
    for _ in range(1000):
        time.sleep(0.1)
        counter.inc.remote()

if __name__ == '__main__':
    ray.init(ignore_reinit_error=True)
    counter = Counter.remote()

    # Start some tasks that use the actor.
    [f.remote(counter) for _ in range(3)]

    # Print the counter value.
    for _ in range(10):
        time.sleep(1)
        print(ray.get(counter.get_counter.remote()))

    ray.shutdown()
