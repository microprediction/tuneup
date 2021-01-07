from tuneup.trivariateobjectives.trivariateboxobjectives import OBJECTIVES, AN_OBJECTIVE
from tuneup.trivariatesingleobjectivesolvers.hyperoptcube import hyperopt_cube

objective, scale = AN_OBJECTIVE


def test_cube():
    for objective, scale in OBJECTIVES.items():
        best = hyperopt_cube(objective=objective,scale=scale,n_trials=5)


if __name__=="__main__":
    test_cube()