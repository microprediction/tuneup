import optuna
from tuneup.util import dilate
from optuna.logging import CRITICAL


def optuna_cube(objective,scale, n_trials):

    def cube_objective(trial):
        u1 = trial.suggest_float('u',1e-6,1-1e-6)
        u2 = trial.suggest_float('u',1e-6,1-1e-6)
        u3 = trial.suggest_float('u',1e-6,1-1e-6)
        return objective(dilate([u1,u2,u3], scale))[0]  # Optuna expects tuple returned by objective func

    optuna.logging.set_verbosity(CRITICAL)
    study = optuna.create_study()
    study.optimize(cube_objective,n_trials=n_trials)
    return study.best_value

