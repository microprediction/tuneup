# A master list of objective functions defined on cubes [-L,L]^d
import deap
from tuneup.filtering import EXPNORM_OBJECTIVES
from deap import benchmarks

# We'll use DEAP's set of groovy benchmarks.
# See pretty pictures at https://deap.readthedocs.io/en/master/api/benchmarks.html#deap.benchmarks
# In the format {function:L}
DEAP_OBJECTIVES = {benchmarks.schaffer:100,
              benchmarks.bohachevsky:100,
              benchmarks.griewank:600,
              benchmarks.h1:100,
              benchmarks.himmelblau:6,
              benchmarks.rastrigin:5.12,
              benchmarks.rastrigin_scaled:5.12,
              benchmarks.rastrigin_skew:5.12,
              benchmarks.schwefel:500}


# But also some from a "real" filtering problem
OBJECTIVES = EXPNORM_OBJECTIVES


OBJECTIVES.update(DEAP_OBJECTIVES)
