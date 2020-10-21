from hyperopt import fmin, hp, tpe, Trials, space_eval, STATUS_OK


# Find best value of trivariateobjectives functions on hypercubes [-scale,+scale]^3

def hyperopt_cube(objective,scale, n_trials, n_dim, with_count=False):

    hp_space = dict( [('u'+str(i), hp.uniform('u'+str(i), -scale,scale)) for i in range(n_dim)])

    global feval_count
    feval_count = 0

    def _objective(hps):
        global feval_count
        feval_count += 1
        us = [ hps['u'+str(i)] for i in range(n_dim)]
        return objective(us)[0]


    trls = Trials()
    res = fmin(_objective, space=hp_space, algo=tpe.suggest, trials=trls, max_evals=n_trials, show_progressbar=False)
    return (trls.best_trial['result']['loss'], feval_count) if with_count else trls.best_trial['result']['loss']



if __name__=='__main__':
    from tuneup.trivariateobjectives.trivariateboxobjectives import OBJECTIVES

    for objective, scale in OBJECTIVES.items():
        print(hyperopt_cube(objective, scale, n_trials=1000, n_dim=5, with_count=True))