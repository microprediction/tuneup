from scipy.optimize import shgo


def shgo_cube(objective,scale, n_trials, n_dim, with_count=False):
    bounds = [(-scale,scale)]*n_dim

    global feval_count
    feval_count = 0

    def _objective(x):
        global feval_count
        feval_count += 1
        return objective(list(x))[0]

    result = shgo(_objective, bounds, options={'maxfev':n_trials,'minimize_every_iter':False,'maxfun':n_trials}, sampling_method='sobol')
    return (result.fun, feval_count) if with_count else result.fun

if __name__ == '__main__':
    from tuneup.trivariateobjectives.trivariateboxobjectives import AN_OBJECTIVE, ANOTHER_OBJECTIVE, OBJECTIVES
    for objective, scale in OBJECTIVES.items():
        print(shgo_cube(objective, scale, n_trials=300, n_dim=5, with_count=True))
