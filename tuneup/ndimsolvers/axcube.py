from ax import optimize
import logging
from logging import CRITICAL
from ax.utils.common.logger import get_root_logger
rt = get_root_logger()
rt.setLevel(CRITICAL)
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore")


def ax_cube(objective,scale, n_trials, n_dim, with_count=False):

    global feval_count
    feval_count = 0

    def evaluation_func(prms):
        global feval_count
        feval_count += 1
        return objective([prms["u"]+str(i) for i in range(n_dim)])[0]

    parameters = [ {
                "name": "u"+str(i),
                "type": "range",
                "bounds": [-scale, scale],
                 } for i in range(n_dim)]
    best_parameters, best_values, experiment, model = optimize( parameters=parameters,
        # Booth function
        evaluation_function=evaluation_func,
        minimize=True,
        total_trials=n_trials)
    return (best_values[0]['objective'], feval_count) if with_count else best_values[0]['objective']



if __name__ == '__main__':
    from tuneup.trivariateobjectives.trivariateboxobjectives import AN_OBJECTIVE, ANOTHER_OBJECTIVE, OBJECTIVES
    for objective, scale in OBJECTIVES.items():
        print(ax_cube(objective, scale, n_trials=10, n_dim=5, with_count=True))
