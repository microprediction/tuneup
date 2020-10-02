import pymoo
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.model.problem import Problem
import numpy as np
from pymoo.factory import get_algorithm, get_termination
from pymoo.util.termination.default import SingleObjectiveDefaultTermination



def test_hello_world():
    problem = get_problem("zdt1")
    algorithm = NSGA2(pop_size=10)
    res = minimize(problem,
                   algorithm,
                   ('n_gen', 10),
                   seed=1,
                   verbose=False)

    plot = Scatter()
    plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
    plot.add(res.F, color="red")
    plot.show()


def pymoo_cube_sortof(n_trials=50):

    class SphereWithConstraint(Problem):

        def __init__(self):
            super().__init__(n_var=10, n_obj=1, n_constr=1, xl=0, xu=1)

        def _evaluate(self, x, out, *args, **kwargs):
            out["F"] = np.sum((x - 0.5) ** 2, axis=1)
            out["G"] = 0.1 - out["F"]

    algorithm = get_algorithm("nsga2")
    termination = get_termination("n_eval", n_trials)
    problem = SphereWithConstraint()

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


if __name__=='__main__':
    pymoo_cube_sortof(n_trials=100)