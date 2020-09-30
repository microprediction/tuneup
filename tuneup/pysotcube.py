import logging
import os.path
from poap.controller import BasicWorkerThread, ThreadController
from pySOT.experimental_design import SymmetricLatinHypercube
from pySOT.strategy import SRBFStrategy
from pySOT.surrogate import CubicKernel, LinearTail, RBFInterpolant
from pySOT.optimization_problems.optimization_problem import OptimizationProblem
import numpy as np


class GenericProblem(OptimizationProblem):

    def __init__(self, dim, objective, scale):
        self.dim = dim
        self.min = 0
        self.minimum = np.zeros(dim)
        self.lb = -scale * np.ones(dim)
        self.ub = scale * np.ones(dim)
        self.int_var = np.array([])
        self.cont_var = np.arange(0, dim)
        self.objective = objective
        self.info = str(dim) + "-dimensional objective function " + objective.__name__

    def eval(self, x):
        """Evaluate the objective x

        :param x: Data point
        :type x: numpy.array
        :return: Value at x
        :rtype: float
        """
        self.__check_input__(x)
        d = float(self.dim)
        return self.objective([x[0],x[1],x[2]])[0]


def pysot_cube(objective=None,scale=None, n_trials=50):

    if False:
        if not os.path.exists("./logfiles"):
            os.makedirs("logfiles")
        if os.path.exists("./logfiles/example_simple.log"):
            os.remove("./logfiles/example_simple.log")
        logging.basicConfig(filename="./logfiles/example_simple.log", level=logging.INFO)

    num_threads = 2
    max_evals = n_trials
    gp = GenericProblem(dim=3, objective=objective,scale=scale)
    rbf = RBFInterpolant(dim=3, lb=np.array([-scale,-scale,-scale]), ub=np.array([scale,scale,scale]), kernel=CubicKernel(), tail=LinearTail(3))
    slhd = SymmetricLatinHypercube(dim=3, num_pts=2 * (3 + 1))

    # Create a strategy and a controller
    controller = ThreadController()
    controller.strategy = SRBFStrategy(
        max_evals=max_evals, opt_prob=gp, exp_design=slhd, surrogate=rbf, asynchronous=True
    )

    # Launch the threads and give them access to the objective function
    for _ in range(num_threads):
        worker = BasicWorkerThread(controller, gp.eval)
        controller.launch_worker(worker)

    # Run the optimization strategy
    result = controller.run()
    return result.value

