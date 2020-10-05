from hyperopt import fmin, hp, tpe, Trials, space_eval, STATUS_OK


# Find best value of trivariateobjectives functions on hypercubes [-scale,+scale]^3

def hyperopt_cube(objective,scale, n_trials, n_dim):

    hp_space = {'u1': hp.uniform('u1', -scale,scale),
                'u2': hp.uniform('u2', -scale,scale),
                'u3': hp.uniform('u3', -scale, scale)}

    hp_space = dict( [('u'+str(i), hp.uniform('u'+str(i), -scale,scale)) for i in range(n_dim)])

    def _objective(hps):
        us = [ hps['u'+str(i)] for i in range(n_dim)]
        return objective(us)[0]


    trls = Trials()
    res = fmin(_objective, space=hp_space, algo=tpe.suggest, trials=trls, max_evals=n_trials, show_progressbar=False)
    return trls.best_trial['result']['loss']



if __name__=='__main__':
    def silly(u):
        return u[0]*u[1]*u[2]+u[5]*2,

    best = hyperopt_cube(objective=silly,scale=1, n_trials=10, n_dim=10)
    print(best)