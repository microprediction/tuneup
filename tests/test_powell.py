from scipy.optimize import minimize
from tuneup.trivariateobjectives.trivariateboxobjectives import AN_OBJECTIVE
from tuneup.trivariatesingleobjectivesolvers.powellcube import powell_cube
from tuneup.trivariatesingleobjectivesolvers.optunacube import optuna_cube


def test_powell_cube():
    objective, scale = AN_OBJECTIVE
    best_value_1 = powell_cube(objective=objective,scale=scale,n_trials=20)
    best_value_2 = optuna_cube(objective=objective, scale=scale, n_trials=20)
    assert abs(best_value_1-best_value_2)<100.
    print(best_value_1)



def test_feval_count(n_dim=6):
    scale = 5
    bounds = [(-scale,scale) ]*n_dim
    global feval_count
    feval_count = 0

    def _objective(x):
        global feval_count
        feval_count += 1
        return x[0]*x[1]*x[1]-3*x[0]+x[2]*x[1]

    result = minimize(_objective, x0=[0.5]*n_dim, method='Powell',bounds=bounds, options={'maxfev':700})
    print(result.fun)
    print(str(feval_count))


if __name__=='__main__':
    test_feval_count(n_dim=30)