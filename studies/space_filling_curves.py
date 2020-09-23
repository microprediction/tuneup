import optuna
from microconventions.zcurve_conventions import ZCurveConventions
from microconventions.stats_conventions import StatsConventions
from collections import Counter
from optuna.logging import CRITICAL
from deap import benchmarks


# This study investigates the performance degredation, if any, when we transfer a function of 2 or 3 variables to a univariate function
# before calling optuna. The conversion is achieved via a space-filling curve.
# See https://www.swarmprediction.com/zcurves.html for a video of a space-filling Z-curve


# We'll use DEAP's set of groovy benchmarks.
# See pretty pictures at https://deap.readthedocs.io/en/master/api/benchmarks.html#deap.benchmarks
OBJECTIVES = {benchmarks.schaffer:100,
              benchmarks.bohachevsky:100,
              benchmarks.griewank:600,
              benchmarks.h1:100,
              benchmarks.himmelblau:6,
              benchmarks.rastrigin:5.12,
              benchmarks.rastrigin_scaled:5.12,
              benchmarks.rastrigin_skew:5.12,
              benchmarks.schwefel:500}


def scale_me(u,scale):
    if isinstance(u,list):
        return [u_*scale for u_ in u]
    else:
        return u*scale

all_counts = Counter()      # All wins broken down by method
overall_counts = Counter()  # Total number of wins for projection
n_trials = 200               # Number of evaluations of the objective function
n_races  = 1600             # Number of times to run the horse race
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


    for iter in range(n_races):
        race = dict()
        for horse in HORSE_RACE:
            study = optuna.create_study()
            study.optimize(horse, n_trials=n_trials)
            race[horse.__name__]=study.best_value
        min_value = max(race.values())  # maximum value
        winners = [k for k, v  in race.items() if v == min_value]

        all_counts.update({objective.__name__+'::'+winners[0]:1})
        overall_counts.update({winners[0]:1})
        current_counts.update({winners[0]:1})
        if iter % 200 ==0:
            print(current_counts)


    print(all_counts)
    print(overall_counts)
    print(current_counts)