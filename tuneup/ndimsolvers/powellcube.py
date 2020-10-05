from scipy.optimize import minimize


def powell_cube(objective,scale, n_trials, n_dim):
    bounds = [(-scale,scale) ]*n_dim

    def _objective(x):
        return objective(list(x))[0]

    result = minimize(_objective, x0=[0]*n_dim, method='Powell',bounds=bounds, options={'maxfev':n_trials})
    return _objective(result.x)




