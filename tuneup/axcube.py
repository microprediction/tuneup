from ax import optimize
import logging
from logging import CRITICAL
from ax.utils.common.logger import get_root_logger
rt = get_root_logger()
rt.setLevel(CRITICAL)
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore")


def ax_cube(objective,scale, n_trials):

    def evaluation_func(prms):
        return objective([prms["u1"],prms["u2"],prms["u3"]])[0]

    best_parameters, best_values, experiment, model = optimize( parameters=[
            {
                "name": "u1",
                "type": "range",
                "bounds": [-scale, scale],
            },
            {
                "name": "u2",
                "type": "range",
                "bounds": [-scale, scale],
            },
            {
                "name": "u3",
                "type": "range",
                "bounds": [-scale, scale],
            },
        ],
        # Booth function
        evaluation_function=evaluation_func,
        minimize=True,
        total_trials=n_trials)
    return best_values[0]['objective']


if __name__=="__main__":
    def objective1(u):
        return u[0]*u[2],
    bv = ax_cube(objective=objective1, scale=5, n_trials=10)
    print(bv)