from tuneup.ndimhorserace import run_race, OutputType
from tuneup.ndimsingleobjectives.ndimboxobjectives import OBJECTIVES
from tuneup.ndimsolvers.ndimboxsolvers import OPEN_SOURCE_SOLVERS, optuna_cube, hyperopt_cube, pysot_cube
from pprint import pprint
import random


def race_specification(debug:bool,output_type:OutputType):
    n_dim = 6 if not debug else 3
    solvers = [optuna_cube, hyperopt_cube, pysot_cube]
    objectives = OBJECTIVES
    objective_thinning = 2 if debug else 1 # e.g. if 3 we use every 3rd objective, on average.
    max_thresholds = 2 if debug else 20
    n_outer_repeat = 1000 if not debug else 5
    n_threshold_repeat = 10 if not debug else 1  # Number of times to call each solver when setting scoring scale
    n_trials = 225 if not debug else 5  # Number of evaluations of the objective function
    n_inner_repeat = 10 if not debug else 2  # Number of times to run the horse race
    max_objectives = 2 if debug else 10
    objectives = dict(([(k, v) for k, v in objectives.items() if random.choice(range(objective_thinning))==0][:max_objectives]))
    threshold_trials = [64,90,128,181,256, 362, 512, 724, 1024, 1448][:max_thresholds]
    spec = {'objectives': objectives,
            'solvers': solvers,
            'threshold_trials': threshold_trials,
            'n_outer_repeat': n_outer_repeat,
            'n_threshold_repeat': n_threshold_repeat,
            'n_trials': n_trials,
            'n_inner_repeat': n_inner_repeat,
            'n_dim':n_dim,
            'solvers_for_thresholds': solvers,
            'output_type':output_type}
    return spec


if __name__=='__main__':
    spec = race_specification(debug=False,output_type=OutputType.html)
    pprint(spec)
    run_race(**spec)