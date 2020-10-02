from platypus import NSGAII, DTLZ2

from platypus import NSGAII, Problem, Real, EvolutionaryStrategy, GeneticAlgorithm

def test_multiobjective():

    def belegundu(vars):
        x = vars[0]
        y = vars[1]
        return [-2*x + y, 2*x + y], [-x + y - 1, x + y - 7]

    problem = Problem(2, 2, 2)
    problem.types[:] = [Real(0, 5), Real(0, 3)]
    problem.constraints[:] = "<=0"
    problem.function = belegundu

    algorithm = NSGAII(problem)
    algorithm.run(100)

def test_singleobjective():

    def trivariate(vars):
        x = vars[0]
        y = vars[1]
        z = vars[2]
        return [-2*x + y*z]
    scale = 5
    problem = Problem(3, 1, 0)
    problem.types[:] = [Real(-scale, scale), Real(-scale, scale), Real(-scale, scale)]
    problem.constraints[:] = "<=0"
    problem.function = trivariate

    algorithm = GeneticAlgorithm(problem)
    algorithm.run(50)
    feasible_solution_obj = [s.objectives[0] for s in algorithm.result if s.feasible]
    best_obj = min(feasible_solution_obj)
    print(best_obj)

if __name__=='__main__':
    test_singleobjective()