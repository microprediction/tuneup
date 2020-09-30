


import logging
import os.path

import numpy as np
from poap.controller import BasicWorkerThread, ThreadController

from pySOT.experimental_design import SymmetricLatinHypercube
from pySOT.optimization_problems import Ackley
from pySOT.strategy import SRBFStrategy
from pySOT.surrogate import CubicKernel, LinearTail, RBFInterpolant


def example_simple():
    if not os.path.exists("./logfiles"):
        os.makedirs("logfiles")
    if os.path.exists("./logfiles/example_simple.log"):
        os.remove("./logfiles/example_simple.log")
    logging.basicConfig(filename="./logfiles/example_simple.log", level=logging.INFO)

    num_threads = 2
    max_evals = 50

    ackley = Ackley(dim=10)
    rbf = RBFInterpolant(dim=ackley.dim, lb=ackley.lb, ub=ackley.ub, kernel=CubicKernel(), tail=LinearTail(ackley.dim))
    slhd = SymmetricLatinHypercube(dim=ackley.dim, num_pts=2 * (ackley.dim + 1))

    # Create a strategy and a controller
    controller = ThreadController()
    controller.strategy = SRBFStrategy(
        max_evals=max_evals, opt_prob=ackley, exp_design=slhd, surrogate=rbf, asynchronous=True
    )


    # Launch the threads and give them access to the objective function
    for _ in range(num_threads):
        worker = BasicWorkerThread(controller, ackley.eval)
        controller.launch_worker(worker)

    # Run the optimization strategy
    result = controller.run()

    print("Best value found: {0}".format(result.value))
    print(
        "Best solution found: {0}\n".format(
            np.array_str(result.params[0], max_line_width=np.inf, precision=5, suppress_small=True)
        )
    )


if __name__ == "__main__":
    example_simple()