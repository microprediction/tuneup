from scipy.optimize import shgo


def shgo_cube(objective,scale, n_trials, n_dim):
    bounds = [(-scale,scale)]*n_dim

    def _objective(x):
        return objective(list(x))[0]

    result = shgo(_objective, bounds, options={'maxfev':n_trials,'minimize_every_iter':False}, sampling_method='sobol')
    return result.fun



