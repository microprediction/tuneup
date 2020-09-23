

# Objective function(s) inspired by filtering problems

from microfilter.univariate.expnormdist import ExpNormDist
from microfilter.univariate.expnormdist import DEFAULT_EXPNORM_PARAMS, DEFAULT_EXPNORM_LOWER, DEFAULT_EXPNORM_UPPER
from microfilter.univariate.noisysim import sim_data
from copy import deepcopy
from functools import partial, update_wrapper
from itertools import permutations

NOISY_DATA = sim_data(chronological=True)
lagged_values = list(reversed(NOISY_DATA))
lagged_times = [1. for _ in NOISY_DATA]


def cube_to_params(xs,v1,v2,v3):
    """
    :param xs:  lie in [-1,1]^3
    """
    variable_names = [v1,v2,v3]
    params = deepcopy(DEFAULT_EXPNORM_PARAMS)
    for x,var in zip(xs,variable_names):
        params[var]=DEFAULT_EXPNORM_LOWER[var]+ 0.5*(x+1)*(DEFAULT_EXPNORM_UPPER[var] - DEFAULT_EXPNORM_LOWER[var])
    return params

def expnorm_objective( xs:[float],v1,v2,v3)->float:
    dist = ExpNormDist()
    params = cube_to_params(xs,v1,v2,v3)
    return dist.loss(lagged_values=lagged_values, lagged_times=lagged_times, params=params),    # Tuple convention as per DEAP


def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func


def make_expnorm_objectives():
     objectives = dict()
     all_vars = ['g1','g2','logK','loc''logScale']
     perms = permutations(all_vars,3)
     for vars in perms:
        objective1 = wrapped_partial(expnorm_objective,v1=vars[0],v2=vars[1],v3=vars[2])
        objective1.__name__ = 'expnorm (varying '+','.join(vars)+')'
        objectives.update({objective1:1})
     return objectives

EXPNORM_OBJECTIVES = make_expnorm_objectives()

