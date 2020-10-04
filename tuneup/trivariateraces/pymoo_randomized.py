from tuneup.horserace import latex_horse_race
from tuneup.trivariatesingleobjectivesolvers.trivariateboxsolvers import PYMOO_SOLVERS, PYMOO_BROKEN
from tuneup.trivariateobjectives.trivariateboxobjectives import OBJECTIVES
from pprint import pprint
import random
import numpy as np

# Not working too well as the PyMoo arguments remain mysterious to me


def random_open_source_race_specification(debug:bool):
    candidate_solvers = [slv for slv in PYMOO_SOLVERS if slv not in PYMOO_BROKEN ]
    objectives = OBJECTIVES
    objective_thinning = 3  # e.g. if 3 we use every 3rd objective, on average.
    num_solvers = 6 if not debug else 3        # How many in the race ??
    max_thresholds = 5 if debug else 20
    n_outer_repeat = 1000 if not debug else 5
    n_threshold_repeat = 5 if not debug else 1  # Number of times to call each solver when setting scoring scale
    n_trials = 50 if not debug else 10  # Number of evaluations of the objective function
    n_inner_repeat = 100 if not debug else 2  # Number of times to run the horse race
    max_objectives = 2 if debug else 10
    objectives = dict(([(k, v) for k, v in objectives.items() if random.choice(range(objective_thinning))==0][:max_objectives]))
    solvers = list(np.random.choice(a=candidate_solvers,size=num_solvers,replace=False))
    threshold_trials = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024][:max_thresholds]
    spec = {'objectives': objectives,
            'solvers': solvers,
            'threshold_trials': threshold_trials,
            'n_outer_repeat': n_outer_repeat,
            'n_threshold_repeat': n_threshold_repeat,
            'n_trials': n_trials,
            'n_inner_repeat': n_inner_repeat,
            'solvers_for_thresholds':solvers}
    return spec


if __name__=='__main__':
    spec = random_open_source_race_specification(debug=False)
    pprint(spec)
    latex_horse_race(**spec)