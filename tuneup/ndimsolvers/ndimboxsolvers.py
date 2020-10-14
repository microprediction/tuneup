from tuneup.ndimsolvers.optunacube import optuna_cube
from tuneup.ndimsolvers.sigoptcube import sigopt_cube
from tuneup.ndimsolvers.hyperoptcube import hyperopt_cube
from tuneup.ndimsolvers.shgocube import shgo_cube
from tuneup.ndimsolvers.powellcube import powell_cube
from tuneup.ndimsolvers.pysotcube import pysot_cube

OPEN_SOURCE_SOLVERS = [ optuna_cube, hyperopt_cube, shgo_cube, powell_cube, pysot_cube ]
VENDOR_SOLVERS = [sigopt_cube]