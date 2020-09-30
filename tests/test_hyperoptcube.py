from tuneup.objective_functions import OBJECTIVES
from tuneup.hyperoptcube import hyperopt_cube

def test_cube():
    for objective, scale in OBJECTIVES.items():
        best = hyperopt_cube(objective=OBJECTIVES[0],scale=scale)
        print(best)