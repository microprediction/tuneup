from pymoo.optimize import minimize
from pymoo.model.problem import Problem
import numpy as np
from pymoo.factory import get_algorithm, get_termination, get_reference_directions

REF_DIRS = get_reference_directions("das-dennis", 1, n_partitions=6)


def brkga_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="brkga")


def nelder_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="nelder-mead")


def cmaes_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="cmaes")


def nsga2_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="nsga2", ref_dirs=REF_DIRS)


def rnsga2_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="rnsga2", ref_dirs=REF_DIRS)


def rnsga3_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="rnsga3", ref_dirs=REF_DIRS)


def unsga3_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="unsga3", ref_dirs=REF_DIRS)


def moead_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="moead", ref_dirs=REF_DIRS)


def pattern_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="pattern-search")


def ctaea_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="ctaea", ref_dirs=REF_DIRS)


def nsga3_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="nsga3", ref_dirs=REF_DIRS)


def de_cube(objective, scale, n_trials):
    return pymoo_cube(objective=objective, scale=scale, n_trials=n_trials, method_name="nsga3")


def pymoo_cube(objective, scale, n_trials, method_name, ref_dirs=None):
    class ObjectiveProblem(Problem):

        def __init__(self):
            super().__init__(n_var=3, n_obj=1, n_constr=0, xl=-scale, xu=scale)

        def _evaluate(self, x, out, *args, **kwargs):
            out["F"] = np.array([objective(u)[0] for u in x])

    try:
        algorithm = get_algorithm(method_name, ref_dirs=ref_dirs)
    except ValueError:
        algorithm = get_algorithm(method_name)
    termination = get_termination("n_eval", n_trials)
    problem = ObjectiveProblem()

    result = minimize(problem=problem,
                      algorithm=algorithm,
                      termination=termination,
                      seed=None,
                      verbose=False,
                      display=None,
                      callback=None,
                      return_least_infeasible=False,
                      save_history=False
                      )
    f_min = result.F[0]
    return f_min


if __name__ == '__main__':
    from tuneup.trivariateobjectives.trivariateboxobjectives import AN_OBJECTIVE

    objective, scale = AN_OBJECTIVE
    print(pymoo_cube(objective, scale, 20))
