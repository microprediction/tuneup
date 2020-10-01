from scipy.optimize import minimize
from tuneup.objective_functions import AN_OBJECTIVE
from tuneup.powellcube import powell_cube
from tuneup.optunacube import optuna_cube


def test_powell_cube():
    objective, scale = AN_OBJECTIVE
    best_value_1 = powell_cube(objective=objective,scale=scale,n_trials=20)
    best_value_2 = optuna_cube(objective=objective, scale=scale, n_trials=20)
    assert abs(best_value_1-best_value_2)<100.


def test_powell():
    scale = 5
    bounds = [(-scale,scale), (-scale, scale), (-scale, scale) ]

    def _objective(x):
        return x[0]*x[1]*x[1]

    result = minimize(_objective, x0=[0,0,0], method='Powell',bounds=bounds, options={'maxfev':20})
    print(result.fun)


if __name__=='__main__':
    test_powell_cube()