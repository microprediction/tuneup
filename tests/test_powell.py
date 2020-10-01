from scipy.optimize import minimize


def test_powell():
    scale = 5
    bounds = [(-scale,scale), (-scale, scale), (-scale, scale) ]

    def _objective(x):
        return x[0]*x[1]*x[1]

    result = minimize(_objective, x0=[0,0,0], method='Powell',bounds=bounds, options={'maxfev':20})
    print(result.fun)


if __name__=='__main__':
    scale = 5
    bounds = [(-scale,scale), (-scale, scale), (-scale, scale) ]

    def _objective(x):
        return x[0]*x[1]*x[1]

    result = minimize(_objective, x0=[0,0,0], method='Powell',bounds=bounds, options={'maxfev':20})
    print(result.fun)
