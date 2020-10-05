from tuneup.ndimsolvers.optunacube import optuna_cube
from tuneup.ndimsolvers.sigoptcube import sigopt_cube
from tuneup.ndimsolvers.hyperoptcube import hyperopt_cube

OPEN_SOURCE_SOLVERS = [ optuna_cube, hyperopt_cube  ]
VENDOR_SOLVERS = [sigopt_cube]