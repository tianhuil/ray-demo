import ray
from hyperopt import hp
from ray import tune
from ray.tune.suggest.hyperopt import HyperOptSearch

def objective(x, a, b):
    return a * (x ** 0.5) + b

def trainable(config):
    # config (dict): A dict of hyperparameters.

    for x in range(20):
        score = objective(x, config["a"], config["b"])

        ray.tune.report(score=score)  # This sends the score to Tune.

space = {
    "a": hp.uniform("a", 0, 1),
    "b": hp.uniform("b", 0, 20),
}

hyperopt = HyperOptSearch(space, metric="score", mode="max")

if __name__ == '__main__':
    ray.init(ignore_reinit_error=True)
    tune.run(
        trainable,
        search_alg=hyperopt,
        num_samples=20,
        stop={"training_iteration": 20},
    )
    run.shutdown()
