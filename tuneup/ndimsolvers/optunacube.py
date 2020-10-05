import optuna
from tuneup.util import dilate
from optuna.logging import CRITICAL


def optuna_cube(objective,scale, n_trials,n_dim):

    def cube_objective(trial):
        us = [ trial.suggest_float('u'+str(i),0,1) for i in range(n_dim)]
        return objective(dilate(us, scale))[0]  # Optuna expects tuple returned by objective func

    optuna.logging.set_verbosity(CRITICAL)
    study = optuna.create_study()
    study.optimize(cube_objective,n_trials=n_trials)
    return study.best_value

if __name__=='__main__':
  from tuneup.ndimsingleobjectives.ndimboxobjectives import AN_OBJECTIVE
  objective, scale = AN_OBJECTIVE
  print(optuna_cube(objective=objective,scale=scale,n_trials=2,n_dim=10))
