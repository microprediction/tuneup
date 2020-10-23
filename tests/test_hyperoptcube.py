from tuneup.trivariateobjectives.trivariateboxobjectives import OBJECTIVES, AN_OBJECTIVE
from tuneup.trivariatesingleobjectivesolvers.hyperoptcube import hyperopt_cube

objective, scale = AN_OBJECTIVE

def test_cube():
    for objective, scale in OBJECTIVES.items():
        best = hyperopt_cube(objective=objective,scale=scale,n_trials=5)
        print(best)


def test_eval_count():
    scale = 5
    bounds = [(-scale,scale)]*6
    global feval_count
    feval_count = 0

    def _objective(x):
        global feval_count
        feval_count += 1
        return hyperopt_cube()

    result = hyperopt_cube(_objective, b)
    print(result.fun)
    print(str(feval_count))


if __name__=="__main__":
    test_cube()