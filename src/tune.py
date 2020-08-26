import ray

def objective(x, a, b):
    return a * (x ** 0.5) + b

def trainable(config):
    # config (dict): A dict of hyperparameters.

    for x in range(20):
        score = objective(x, config["a"], config["b"])

        ray.tune.report(score=score)  # This sends the score to Tune.

if __name__ == '__main__':
    ray.init()
