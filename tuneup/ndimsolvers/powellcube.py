from scipy.optimize import minimize


def powell_cube(objective,scale, n_trials, n_dim, with_count=False):
    bounds = [(-scale,scale) ]*n_dim


    global feval_count
    feval_count = 0

    def _objective(x):
        global feval_count
        feval_count +=1
        return objective(list(x))[0]

    result = minimize(_objective, x0=[0]*n_dim, method='Powell',bounds=bounds, options={'maxfev':n_trials})
    return (_objective(result.x), feval_count) if with_count else feval_count




