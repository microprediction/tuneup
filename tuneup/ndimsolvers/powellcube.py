from scipy.optimize import minimize

global feval_count
feval_count=0

def powell_cube(objective,scale, n_trials, n_dim, with_count=False):
    bounds = [(-scale,scale) ]*n_dim


    global feval_count
    feval_count = 0

    def _objective(x):
        global feval_count
        feval_count +=1
        return objective(list(x))[0]

    result = minimize(_objective, x0=[0]*n_dim, method='powell',bounds=bounds, options={'maxfev':n_trials,'maxiter':n_trials,'maxfun':n_trials})
    return (_objective(result.x), feval_count) if with_count else _objective(result.x)




if __name__ == '__main__':
    from tuneup.trivariateobjectives.trivariateboxobjectives import AN_OBJECTIVE, ANOTHER_OBJECTIVE, OBJECTIVES



    for objective, scale in OBJECTIVES.items():
        print(powell_cube(objective, scale, n_trials=5, n_dim=50, with_count=True))
