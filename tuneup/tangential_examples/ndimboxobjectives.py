# A master list of objective functions defined on cubes [-scale,scale]^3

from deap import benchmarks

# We'll use DEAP's set of groovy benchmarks.
# See pretty pictures at https://deap.readthedocs.io/en/master/api/benchmarks.html#deap.benchmarks
# In the format {function:scale}

DEAP_OBJECTIVES = {benchmarks.schaffer:100,
                   benchmarks.sphere:1,
              benchmarks.bohachevsky:100,
              benchmarks.griewank:600,
              benchmarks.rastrigin:5.12,
              benchmarks.rastrigin_scaled:5.12,
              benchmarks.rastrigin_skew:5.12,
              benchmarks.schwefel:500,
                   benchmarks.rosenbrock:5}

AN_OBJECTIVE = (benchmarks.schwefel,5.12)

# But also some from a "real" filtering problem
OBJECTIVES = DEAP_OBJECTIVES
