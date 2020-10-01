from scipy.optimize import shgo


def shgo_cube(objective,scale, n_trials):
    bounds = [(-scale,scale), (-scale, scale), (-scale, scale) ]

    def _objective(x):
        return objective([x[0],x[1],x[2]])[0]

    result = shgo(_objective, bounds, options={'maxfev':n_trials}, sampling_method='sobol')
    return result.fun



