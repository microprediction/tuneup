from hyperopt import fmin, hp, tpe, Trials, space_eval, STATUS_OK


# Find best value of trivariateobjectives functions on hypercubes [-scale,+scale]^3

def hyperopt_cube(objective,scale, n_trials):

    hp_space = {'u1': hp.uniform('u1', -scale,scale),
                'u2': hp.uniform('u2', -scale,scale),
                'u3': hp.uniform('u3', -scale, scale)}

    def _objective(hps):
        return objective([hps['u1'], hps['u2'],hps['u3']])[0]


    trls = Trials()
    res = fmin(_objective, space=hp_space, algo=tpe.suggest, trials=trls, max_evals=n_trials, show_progressbar=False)
    return trls.best_trial['result']['loss']



if __name__=='__main__':
    def silly(u):
        return u[0]*u[1]*u[2],

    best = hyperopt_cube(objective=silly,scale=1, n_trials=10)
    print(best)