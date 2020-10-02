import optuna
from microconventions.zcurve_conventions import ZCurveConventions
from microconventions.stats_conventions import StatsConventions
from collections import Counter
from tuneup.objective_functions import DEAP_OBJECTIVES as OBJECTIVES
from microprediction.univariate.runningmoments import RunningVariance
import pandas as pd
from pprint import pprint
from tuneup.optunacube import optuna_cube
from tuneup.hyperoptcube import hyperopt_cube
from tuneup.pysotcube import pysot_cube
import numpy as np
from tuneup.util import chop, escape_bs_and_ff
from tuneup.shgocube import shgo_cube
from tuneup.powellcube import powell_cube
from tuneup.axcube import ax_cube
from tuneup.sigoptcube import sigopt_cube

# Comparing open source black box optimizers

SOLVERS = [sigopt_cube, powell_cube, shgo_cube, optuna_cube]


#------------
#   Config
#------------


DEBUG = False
REVERSE_OBJECTIVES = True
MAX_OBJECTIVES = 2 if DEBUG else 2
MAX_RATINGS = 5 if DEBUG else 20
n_outer_repeats = 1000
n_benchmark_repeats = 3 if not DEBUG else 1   # Number of times to call each solver when setting scoring scale
n_trials = 50 if not DEBUG else 10            # Number of evaluations of the objective function
n_races  = 100 if not DEBUG else 2             # Number of times to run the horse race



#------------
#   Race
#------------


OBJECTIVES = dict(reversed([(k,v) for k,v in OBJECTIVES.items()][:MAX_OBJECTIVES]))
all_counts = Counter()      # All wins broken down by method
overall_counts = Counter()  # Total number of wins for projection
N_BENCHMARK_TRIALS = [1,2,4,8,16,32,64,128,256,512][:MAX_RATINGS]
N_BENCHMARK_TRIALS_str = ' To create a quantized performance scale we averaged the best objective value when $n$ trials were allowed optimizing $F$, where $n$ was chosen from '+\
                         ','.join([str(trl) for trl in N_BENCHMARK_TRIALS[:-1]])+' and '+str(N_BENCHMARK_TRIALS[-1])+\
                         '. A win or loss indicates that the search was better, or worse, by an amount that would normally be commensurate with a doubling of computation time, at least.'

ratings_df = pd.DataFrame()


performance = dict()
good_scores_cache = dict()

def print_start_of_table():
    print(' ')
    print(' ')
    print( escape_bs_and_ff("""
       \begin{table}[]
    \centering
    \begin{tabular}{"""))
    print( '|c'*(len(SOLVERS)+1)+ "|}  ")
    print(' \hline')
    print( ' Objective & ' +  ' & '.join([ solver.__name__.replace('_cube','') for solver in SOLVERS ]) + ' \\\\ ')
    print(' \hline ')

def print_end_of_table():
    print("""  \hline
     \end{tabular}
    \caption{CAPTION}
    \label{tab:my_label}
     \end{table}""")


for outer_iter in range(n_outer_repeats):
    if outer_iter>0:
        print_start_of_table()
    for objective, scale in OBJECTIVES.items():
        obj_performance = dict()

        # First get an idea of what is reasonable and determine a performance scale
        if objective.__name__ in good_scores_cache:
            good_scores = good_scores_cache[objective.__name__]
        else:
            print(' ')
            print('Computing rating scale for '+objective.__name__)
            good_scores = list()
            for n_benchmark_trials in N_BENCHMARK_TRIALS:
                the_best_values = list()
                for _ in range(n_benchmark_repeats):
                    f_values = [ solver(objective,scale,n_trials=n_benchmark_trials) for solver in SOLVERS ]
                    the_best_values.append(np.mean(f_values))
                good_scores.append(np.mean(the_best_values))
                print(good_scores)
            good_scores_cache[objective.__name__] = good_scores

        def compute_rating(score):
            return sum([score<good_score for good_score in good_scores])

        # Then run horse race with quantized scoring
        for iter in range(n_races):
            for solver in SOLVERS:
                performance_key = objective.__name__+'::'+(solver.__name__.replace('_cube',''))
                best_value = solver(objective=objective,scale=scale,n_trials=n_trials)
                rating = compute_rating(best_value)
                if performance_key not in performance:
                    performance[performance_key] = RunningVariance()
                if performance_key not in obj_performance:
                    obj_performance[performance_key] = performance[performance_key]
                performance[performance_key].update(rating)

        print( objective.__name__ + ' & ' + ' & '.join( [ '$'+chop(p.mean) + "\pm" + chop(p.std())+'$' for ky,p in obj_performance.items() if objective.__name__ in ky]) + ' \\\\ ')

    if outer_iter>0:
        print_end_of_table()