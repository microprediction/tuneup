from tuneup.trivariatesingleobjectivesolvers.optunacube import optuna_cube
from tuneup.trivariatesingleobjectivesolvers.hyperoptcube import hyperopt_cube
from tuneup.trivariatesingleobjectivesolvers.pysotcube import pysot_cube
from tuneup.trivariatesingleobjectivesolvers.shgocube import shgo_cube
from tuneup.trivariatesingleobjectivesolvers.powellcube import powell_cube
from tuneup.trivariatesingleobjectivesolvers.axcube import ax_cube
from tuneup.trivariatesingleobjectivesolvers.platypuscube import genetic_cube, evolutionary_cube
from tuneup.trivariatesingleobjectivesolvers.pymoocube import brkga_cube, pattern_cube, nelder_cube, cmaes_cube
from tuneup.trivariatesingleobjectivesolvers.sigoptcube import sigopt_cube

OPEN_SOURCE_SOLVERS = [genetic_cube, evolutionary_cube,
                       nelder_cube, cmaes_cube,
                       ax_cube, powell_cube,
                       brkga_cube, pattern_cube,
                       shgo_cube, hyperopt_cube,
                       optuna_cube, pysot_cube]


VENDOR_SOLVERS = [sigopt_cube]

GOOD_AT_DEAP = [powell_cube, shgo_cube, optuna_cube]
GOOD_SOLVERS = [shgo_cube, optuna_cube, hyperopt_cube, pysot_cube]