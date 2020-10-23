from scipy.optimize import rosen, shgo, minimize


def test_shgo():
    bounds = [(0,2)]*6
    result = shgo(rosen, bounds,options={'fevmax':20})
    result.x, result.fun
    print(result.fun)


feval_count = 0

def test_eval_count():
    scale = 5
    bounds = [(-scale,scale)]*6
    global feval_count
    feval_count = 0

    def _objective(x):
        global feval_count
        feval_count += 1
        return x[0]*x[1]*x[1]-3*x[0]

    result = shgo(_objective, bounds, options={'maxfev':700}, sampling_method='sobol')
    print(result.fun)
    print(str(feval_count))




if __name__=='__main__':
    test_eval_count()