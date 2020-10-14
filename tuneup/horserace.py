from collections import Counter
from microprediction.univariate.runningmoments import RunningVariance
import numpy as np
from tuneup.util import comma_and, solver_name, escape_bs_and_ff, chop


def latex_horse_race(objectives:dict,  # {<solver>:scale, <solver>:scale}
                     solvers:list,
                     threshold_trials:[float],
                     n_outer_repeat:int,
                     n_threshold_repeat:int,
                     n_trials:int,
                     n_inner_repeat:int,
                     solvers_for_thresholds=None):
    """ Creates a continuously updating table that can be pasted directly into latex document """

    if solvers_for_thresholds is None:
        solvers_for_thresholds = objectives

    CAPTION = 'Comparison between '+ comma_and([solver_name(solver) for solver in solvers]) + \
              ' where $N='+str(n_trials)+ """$ function evaluations are permitted. 
              To create a quantized performance scale we averaged the best objective
               value when $n$ trials were allowed optimizing $F$, where $n$ was chosen from """ + \
                 comma_and(threshold_trials) + \
                """. A difference of $\pm 1$ indicates that minimum was better, or worse, by an amount
                     that would normally be commensurate with a doubling of computation time.
                """

    performance = dict()
    good_scores_cache = dict()

    def print_start_of_table():
        print(' ')
        print(' ')
        print(escape_bs_and_ff("""
           \begin{table}[]
        \centering
        \begin{tabular}{"""))
        print('|c' * (len(solvers) + 1) + "|}  ")
        print(' \hline')
        print(' Objective & ' + ' & '.join([solver.__name__.replace('_cube', '') for solver in solvers]) + ' \\\\ ')
        print(' \hline ')

    def print_end_of_table():
        print("""  \hline
         \end{tabular}
        \caption{CAPTION}
        \label{tab:my_label}
         \end{table}""".replace('CAPTION',CAPTION))

    for outer_iter in range(n_outer_repeat):
        if outer_iter > 0:
            print_start_of_table()
        for objective, scale in objectives.items():
            obj_performance = dict()

            # First get an idea of what is reasonable and determine a performance scale
            if objective.__name__ in good_scores_cache:
                good_scores = good_scores_cache[objective.__name__]
            else:
                print(' ')
                print('Computing rating scale for ' + objective.__name__)
                good_scores = list()
                for n_benchmark_trials in threshold_trials:
                    the_best_values = list()
                    for _ in range(n_threshold_repeat):
                        f_values = [v for v,c in [ solver(objective, scale, n_trials=n_benchmark_trials, with_count=True) for solver in solvers_for_thresholds] if c<1.2*n_benchmark_trials]
                        the_best_values.append(np.mean(f_values))
                    good_scores.append(np.mean(the_best_values))
                    print(good_scores)
                good_scores_cache[objective.__name__] = good_scores

            def compute_rating(score):
                return sum([score < good_score for good_score in good_scores])

            # Then run horse race with quantized scoring
            for iter in range(n_inner_repeat):
                for solver in solvers:
                    performance_key = objective.__name__ + '::' + (solver.__name__.replace('_cube', ''))
                    best_value, f_count = solver(objective=objective, scale=scale, n_trials=n_trials, with_scores=True)
                    if f_count<1.2*n_trials:
                        rating = compute_rating(best_value)
                        if performance_key not in performance:
                            performance[performance_key] = RunningVariance()
                        if performance_key not in obj_performance:
                            obj_performance[performance_key] = performance[performance_key]
                        performance[performance_key].update(rating)
                    else:
                        pass

            print(objective.__name__.replace('_skew', ' (skew)').replace('_scaled', ' (scaled) ') + ' & ' + ' & '.join(
                ['$' + chop(p.mean) + "\pm" + chop(p.std()) + '$' for ky, p in obj_performance.items() if
                 objective.__name__ in ky]) + ' \\\\ ')

        if outer_iter > 0:
            print_end_of_table()
