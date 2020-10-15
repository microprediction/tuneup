from tuneup.ndimhorserace import run_race, OutputType, bad_versus_good
from tuneup.ndimsingleobjectives.ndimboxobjectives import OBJECTIVES
from tuneup.ndimsolvers.pymoocube import PYMOO_GOOD, nsga2_cube
from tuneup.ndimsolvers.ndimboxsolvers import OPEN_SOURCE_SOLVERS, optuna_cube, hyperopt_cube, pysot_cube, genetic_cube
import random
from pprint import pprint

def race_specification(debug:bool):
    n_dim = 20 if not debug else 3
    n_trials = 500 if not debug else 3
    bad_solver = nsga2_cube # Does not do the right number of function evals
    good_solvers = [pysot_cube]+PYMOO_GOOD
    objectives = OBJECTIVES
    objective_thinning = 2 if debug else 1 # e.g. if 3 we use every 3rd objective, on average.
    n_outer_repeat = 1000 if not debug else 5
    n_inner_repeat = 5 if not debug else 2  # Number of times to run the horse race
    max_objectives = 2 if debug else 10
    objectives = dict(([(k, v) for k, v in objectives.items() if random.choice(range(objective_thinning))==0][:max_objectives]))
    spec = {'objectives': objectives,
            'good_solvers': good_solvers,
            'bad_solver':bad_solver,
            'n_outer_repeat': n_outer_repeat,
            'n_trials': n_trials,
            'n_inner_repeat': n_inner_repeat,
            'n_dim':n_dim}
    return spec


if __name__=='__main__':
    spec = race_specification(debug=False)
    pprint(spec)
    bad_versus_good(**spec)