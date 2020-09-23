import optuna
from microconventions.zcurve_conventions import ZCurveConventions
from microconventions.stats_conventions import StatsConventions
from deap import benchmarks
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import math


# A closer look at why space filling curve does well for himelblau example


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

if __name__=='__main__':

    fig, axs = plt.subplots(nrows=3,ncols=3)
    for plot_no, (objective, scale) in enumerate( OBJECTIVES.items()):
        row, col = plot_no % 3, math.floor(plot_no/3)

        def univariate(u):
            z = StatsConventions.norminv(u)
            u2 = zc.from_zcurve(zvalue=z, dim=3)
            return objective(scale_me(u2,scale))[0]


        zc = ZCurveConventions()
        u_values = np.linspace(0,1,1000)
        f_values = [ univariate(u) for u in u_values ]
        axs[row, col].plot(u_values,f_values)
        axs[row, col].set_xlabel(objective.__name__)
    plt.show()

