from scipy.optimize import minimize


def powell_cube(objective,scale, n_trials):
    bounds = [(-scale,scale), (-scale, scale), (-scale, scale) ]

    def _objective(x):
        return objective([x[0],x[1],x[2]])[0]

    result = minimize(_objective, x0=[0,0,0], method='Powell',bounds=bounds, options={'maxfev':n_trials})
    return _objective(result.x)




