from scipy.optimize import rosen, shgo


def test_shgo():
    bounds = [(0,2), (0, 2), (0, 2), (0, 2), (0, 2)]
    result = shgo(rosen, bounds,options={'fevmax':20})
    result.x, result.fun
    print(result.fun)

if __name__=='__main__':
    test_shgo()