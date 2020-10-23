from collections import Counter
from microprediction.univariate.runningmoments import RunningVariance
import numpy as np
from tuneup.util import comma_and, solver_name, escape_bs_and_ff, chop
from enum import Enum
from pprint import pprint

class OutputType(Enum):
    latex = 0
    html = 1



def performance_html_table(performance):
    table = """<div data-hs-responsive-table="true" style="overflow-x: auto; max-width: 100%; width: 100%;">
<table border="2" cellpadding="4" style="width: 100%; border-color: #99acc2; border-style: solid; border-collapse: collapse; table-layout: fixed; height: 434px;">
<tbody>"""

    solvers = set()
    objs = set()
    for ky, pf in performance.items():
        obj,solver = ky.split('::')
        solvers.add(solver)
        objs.add(obj)

    first_row = '<tr><td></td><td>' + '</td><td>'.join(solvers)+'</td></tr>'
    table = table + first_row
    for obj in objs:
        data = list()
        for solver in solvers:
            ky = obj+"::"+solver
            if ky in performance:
                pf = performance[ky]
                data.append(chop(pf.mean)+'+/-'+chop(pf.std()))
            else:
                data.append('N/A')
        table = table +  '<tr><td>'+obj+'</td><td>' + '</td><td>'.join(data)+'</td></tr>'

    table = table + """</tbody></table>
                        </div>"""
    return table

def bad_versus_good(objectives:dict,  # {<solver>:scale, <solver>:scale}
                     bad_solver,
                     good_solvers:list,
                     n_outer_repeat:int,
                     n_trials:int,
                     n_inner_repeat:int,
                     n_dim:int,**ignored):
    """
         Runs naughty solver, captures number of actual function evaluations, and then compares to well behaved solvers
    """
    def obj_solver_key(objective,solver):
        obj_key = objective.__name__.replace('_skew', ' (skew)').replace('_scaled', ' (scaled) ')
        solver_key = (solver.__name__.replace('_cube', ''))
        return obj_key+'::'+solver_key

    bad_and_good = [bad_solver]+good_solvers
    performance = dict()
    feval_counts = RunningVariance()
    for _ in range(n_outer_repeat):
        for objective, scale in objectives.items():
            for _ in range(n_inner_repeat):
                f_bad_min,f_bad_count = bad_solver(objective, scale, n_trials=n_trials, n_dim=n_dim, with_count=True)
                feval_counts.update(f_bad_count)
                f_good_mins = [ solver(objective, scale, n_trials=f_bad_count, n_dim=n_dim, with_count=False) for solver in good_solvers]
                all_mins = [f_bad_min]+f_good_mins
                all_res = [ (obj_solver_key(objective, slvr),min_val) for slvr,min_val in zip(bad_and_good,all_mins) ]
                for ky,val in all_res:
                    if ky not in performance:
                        performance[ky] = RunningVariance()
                    performance[ky].update(val)
        pprint(performance)
        print(' ...based on feval_counts ... ')
        print(feval_counts)
        print(' ')
        print(performance_html_table(performance))
        print(' ')
        print(' ')





def run_race(objectives:dict,  # {<solver>:scale, <solver>:scale}
                     solvers:list,
                     threshold_trials:[float],
                     n_outer_repeat:int,
                     n_threshold_repeat:int,
                     n_trials:int,
                     n_inner_repeat:int,
                     n_dim:int,
                     solvers_for_thresholds=None,
                     output_type:OutputType=OutputType.latex):
    """ Creates a continuously updating table that can be pasted directly into latex document
         TODO: Refactor this steaming pile of shit
    """

    if solvers_for_thresholds is None:
        solvers_for_thresholds = objectives


    performance = dict()
    good_scores_cache = dict()

    def latex_caption():
         return 'Comparison between '+ comma_and([solver_name(solver) for solver in solvers]) + \
                  ' in '+str(n_dim)+' dim, where $N='+str(n_trials)+ """$ function evaluations are permitted.
                   To create a quantized performance scale we averaged the best objective
                   value when $n$ trials were allowed optimizing $F$, where $n$ was chosen from """ + \
                     comma_and(threshold_trials) + \
                    """. A difference of $\pm 1$ indicates that minimum was better, or worse, by an amount
                         that would normally be commensurate with a doubling of computation time.
                    """



    def latex_start_table():
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

    def html_start_table():
        print("""<div data-hs-responsive-table="true" style="overflow-x: auto; max-width: 100%; width: 100%;">
<table border="2" cellpadding="4" style="width: 100%; border-color: #99acc2; border-style: solid; border-collapse: collapse; table-layout: fixed; height: 434px;">
<tbody>""")
        print('<tr><td></td>'+' '.join(['<td>'+'</td><td>'.join([solver.__name__.replace('_cube', '') for solver in solvers])])+'</td>')

    def latex_end_table():
        print("""  \hline
         \end{tabular}
        \caption{CAPTION}
        \label{tab:my_label}
         \end{table}""".replace('CAPTION',latex_caption()))

    def html_end_table():
        print("""
            </tbody>
            </table>""")
        print(' ')

    for outer_iter in range(n_outer_repeat):
        if outer_iter > 0:
            if output_type==OutputType.latex:
                latex_start_table()
            else:
                html_start_table()
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
                        f_values = [v for v,c in [ solver(objective, scale, n_trials=n_benchmark_trials, n_dim=n_dim
                                                   , with_count=True) for solver in solvers_for_thresholds] if c<1.2*n_benchmark_trials]
                        if f_values:
                            the_best_values.append(np.mean(f_values))
                        else:
                            raise Exception('No algorithms got the right number of f evals. Can''t compute benchmark.')
                    good_scores.append(np.mean(the_best_values))
                    print(good_scores)
                good_scores_cache[objective.__name__] = good_scores

            def compute_rating(score):
                return sum([score < good_score for good_score in good_scores])

            # Then run horse race with quantized scoring
            for iter in range(n_inner_repeat):
                for solver in solvers:
                    performance_key = objective.__name__ + '::' + (solver.__name__.replace('_cube', ''))
                    tries_left = 6
                    n_adj_trials = n_trials
                    while tries_left:
                        tries_left -= 1
                        best_value,f_count = solver(objective=objective, scale=scale, n_trials=n_adj_trials, n_dim=n_dim, with_count=True)
                        if f_count<1.1*n_trials:
                            rating = compute_rating(best_value)
                            if performance_key not in performance:
                                performance[performance_key] = RunningVariance()
                            if performance_key not in obj_performance:
                                obj_performance[performance_key] = performance[performance_key]
                            performance[performance_key].update(rating)
                        else:
                            n_adj_trials = int( n_adj_trials*0.7 )



            if output_type==OutputType.latex:
                print(objective.__name__.replace('_skew', ' (skew)').replace('_scaled', ' (scaled) ') + ' & ' + ' & '.join(
                    ['$' + chop(p.mean) + "\pm" + chop(p.std()) + '$' for ky, p in obj_performance.items() if
                     objective.__name__ in ky]) + ' \\\\ ')
            else:
                print('<tr><td>'+objective.__name__.replace('_skew', ' (skew)').replace('_scaled', ' (scaled) ')+ '</td> '+' '.join( ['<td style="width: 25%;">'+chop(p.mean)+'+/-'+chop(p.std())+'</td> ' for ky,p in obj_performance.items() if objective.__name__ in ky]) + '</tr> ')

        if outer_iter > 0:
            if output_type==OutputType.latex:
                latex_end_table()
            else:
                html_end_table()
                print(' ')
                print(latex_caption())
                print(' ')
                print(' ')


