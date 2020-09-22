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
OBJECTIVES = [benchmarks.schaffer, benchmarks.rastrigin_scaled, benchmarks.rastrigin_skew, benchmarks.rastrigin, benchmarks.rosenbrock,
              benchmarks.ackley, benchmarks.cigar, benchmarks.griewank, benchmarks.h1, benchmarks.himmelblau, benchmarks.rastrigin, benchmarks.fonseca,
              benchmarks.schaffer_mo, benchmarks.zdt1, benchmarks.zdt2, benchmarks.zdt3, benchmarks.zdt4, benchmarks.zdt6]


all_counts = Counter()      # All wins broken down by method
overall_counts = Counter()  # Total number of wins for projection
n_trials = 20               # Number of evaluations of the objective function
n_races  = 500              # Number of times to run the horse race
for objective in OBJECTIVES:
    current_counts = Counter()

    print(objective.__name__)

    zc = ZCurveConventions()

    def univariate_bivariate(trial):
        u = trial.suggest_float('u',1e-6,1-1e-6)
        z = StatsConventions.norminv(u)
        u2 = zc.from_zcurve(zvalue=z, dim=2)
        return objective(u2)[0]

    def univariate_trivariate(trial):
        u = trial.suggest_float('u',1e-6,1-1e-6)
        z = StatsConventions.norminv(u)
        u2 = zc.from_zcurve(zvalue=z, dim=3)

        return objective(u2)[0]

    def trivariate(trial):
        u1 = trial.suggest_float('u1',1e-6,1-1e-6)
        u2 = trial.suggest_float('u2',1e-6,1-1e-6)
        u3 = trial.suggest_float('u3',1e-6,1-1e-6)
        u = [u1,u2,u3]
        return objective(u)[0]


    def bivariate(trial):
        u1 = trial.suggest_float('u1',1e-6,1-1e-6)
        u2 = trial.suggest_float('u2',1e-6,1-1e-6)
        u = [u1,u2]
        return objective(u)[0]


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
        if iter % 100 ==0:
            print(current_counts)


    print(all_counts)
    print(overall_counts)
    print(current_counts)