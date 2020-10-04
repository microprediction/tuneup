import optuna
from microconventions.zcurve_conventions import ZCurveConventions
from microconventions.stats_conventions import StatsConventions
from collections import Counter
from optuna.logging import CRITICAL
from tuneup.trivariateobjectives.trivariateboxobjectives import OBJECTIVES


# This study investigates the performance degredation, if any, when we transfer a function of 2 or 3 variables to a univariate function
# before calling optuna. The conversion is achieved via a space-filling curve.
# See https://www.swarmprediction.com/zcurves.html for a video of a space-filling Z-curve


TIE = 1e-3   # Tie tolerance
import numpy as np

def capitalize(word):
    return word[0].upper()+word[1:]

def scale_me(u,scale):
    if isinstance(u,list):
        return [u_*scale for u_ in u]
    else:
        return u*scale


all_counts = Counter()      # All wins broken down by method
overall_counts = Counter()  # Total number of wins for projection
n_trials = 20               # Number of evaluations of the objective function
n_races  = 10000            # Number of times to run the horse race
N_BENCHMARK_TRIALS = [1,2,4,8,16,32,64,128,256][:5]
N_BENCHMARK_TRIALS_str = ' To create a quantized performance scale we averaged the best objective value when $n$ trials were allowed optimizing $F$, where $n$ was chosen from '+\
                         ','.join([str(trl) for trl in N_BENCHMARK_TRIALS[:-1]])+' and '+str(N_BENCHMARK_TRIALS[-1])+\
                         '. A win or loss indicates that the search was better, or worse, by an amount that would normally be commensurate with a doubling of computation time, at least.'

for objective,scale in OBJECTIVES.items():
    current_counts = Counter()

    print(' ')
    print(' ')
    print(objective.__name__)
    print(n_trials)

    zc = ZCurveConventions()

    def univariate_bivariate(trial):
        u = trial.suggest_float('u',1e-6,1-1e-6)
        z = StatsConventions.norminv(u)
        u2 = zc.from_zcurve(zvalue=z, dim=2)
        return objective(scale_me(u2,scale))[0]

    def univariate_trivariate(trial):
        u = trial.suggest_float('u',1e-6,1-1e-6)
        z = StatsConventions.norminv(u)
        u2 = zc.from_zcurve(zvalue=z, dim=3)
        return objective(scale_me(u2,scale))[0]

    def trivariate(trial):
        u1 = trial.suggest_float('u1',1e-6,1-1e-6)
        u2 = trial.suggest_float('u2',1e-6,1-1e-6)
        u3 = trial.suggest_float('u3',1e-6,1-1e-6)
        u = [u1,u2,u3]
        return objective(scale_me(u,scale))[0]


    def bivariate(trial):
        u1 = trial.suggest_float('u1',1e-6,1-1e-6)
        u2 = trial.suggest_float('u2',1e-6,1-1e-6)
        u = [u1,u2]
        return objective(scale_me(u,scale))[0]


    HORSE_RACE = [univariate_trivariate, trivariate]
    optuna.logging.set_verbosity(CRITICAL)


    # First optimize to get an idea of what is reasonable and determine a performance scale
    study = optuna.create_study()
    good_scores = list()
    for n_benchmark_trials in N_BENCHMARK_TRIALS:
        the_best_values = list()
        num_samples = 50 if n_benchmark_trials<=3*n_trials else 10
        for _ in range(num_samples):
            study.optimize(HORSE_RACE[1],n_trials=n_benchmark_trials)
            the_best_values.append(study.best_value)
        good_scores.append(np.mean(the_best_values))
        print(good_scores)

    def rating(score):
        return sum([score<good_score for good_score in good_scores])

    for iter in range(n_races):
        race = dict()
        for horse in HORSE_RACE:
            study = optuna.create_study()
            study.optimize(horse, n_trials=n_trials)
            race[horse.__name__]=rating(study.best_value)

        min_value = max(race.values())  # maximum value

        close = [k for k, v  in race.items() if abs(v-min_value)<TIE]
        if len(close)==2:
            all_counts.update({objective.__name__+'::draw':1})
            overall_counts.update({'draw':1})
            current_counts.update({'draw':1})
        elif len(close)==1:
            winner = close[0]
            all_counts.update({objective.__name__+'::'+winner:1})
            overall_counts.update({winner:1})
            current_counts.update({winner:1})
        if iter % 50 ==0:
            print(current_counts)


    print(all_counts)
    print(overall_counts)
    print(current_counts)



def escape_bs_and_ff(s):
    return s.replace("\b", "\\b").replace("\f", "\\f")

# Latex table of results
winner = 'univariate_trivariate'
loser = 'trivariateobjectives'
ltx = """ \begin{table}[]
    \centering
    \begin{tabular}{|l|c|c|c|c|}
    \hline
        Objective $F$ & Win & Draw & Loss & W/L \\\\
        \hline
     """
for objective in OBJECTIVES:
    wins = all_counts[objective.__name__+'::'+winner]
    draws = all_counts[objective.__name__+"::draw"]
    losses = all_counts[objective.__name__+'::'+loser]
    if losses>0:
        ratio_str = '$ '+str(round(wins/losses,ndigits=2))+' $ '
    elif wins>0 and losses==0:
        ratio_str = ' $ \infty $'
    else:
        ratio_str = ' '
    ltx += capitalize(objective.__name__) + ' & ' + '& '.join([str(j) for j in [wins,draws,losses]]) + ' & ' + ratio_str +  '\\\\ \hline '

ltx +=  r"""\end{tabular}
    \caption{We tabulate how often use of a space filling curve helps (win column) or harms (loss column) a global
    optimization performed by the Optuna library. Some classic objective functions were borrowed from the DEAP collection of benchmarks. We also included optization problems motivated by
    time series prediction parameter estimation. The optimization is permitted to run to
    to $N$ function evaluations, first using a direct optimization of a trivariateobjectives function $F$ and then subsequently an equivalent univariate function $f$.""" + N_BENCHMARK_TRIALS_str + """
     }
    \label{tab:horseraceN}
\end{table}"""


ltx = ltx.replace('_scaled',' (scaled)').replace('_skew',' (skew)').replace('N',str(n_trials)).replace('N',str(n_trials))

print(' ')
print(escape_bs_and_ff(ltx))
pass