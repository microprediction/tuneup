from platypus import NSGAII, Problem, Real, EvolutionaryStrategy, GeneticAlgorithm


def evolutionary_cube(objective,scale,n_trials):
    return platypus_cube(objective=objective,scale=scale,n_trials=n_trials,strategy=EvolutionaryStrategy)

def genetic_cube(objective,scale,n_trials):
    return platypus_cube(objective=objective,scale=scale,n_trials=n_trials,strategy=GeneticAlgorithm)


def platypus_cube(objective,scale, n_trials, strategy):

    def _objective(vars):
        u1 = vars[0]
        u2 = vars[1]
        u3 = vars[2]
        return objective([u1,u2,u3])[0]

    problem = Problem(3, 1, 0)
    problem.types[:] = [Real(-scale, scale), Real(-scale, scale), Real(-scale, scale)]
    problem.constraints[:] = "<=0"
    problem.function = _objective

    algorithm = strategy(problem)
    algorithm.run(n_trials)
    feasible_solution_obj = [s.objectives[0] for s in algorithm.result if s.feasible]
    best_obj = min(feasible_solution_obj)
    return best_obj


if __name__ == '__main__':
    from tuneup.trivariateobjectives.trivariateboxobjectives import OBJECTIVES

    for objective, scale in OBJECTIVES.items():
        print(evolutionary_cube(objective, scale, n_trials=5))
        print(genetic_cube(objective, scale, n_trials=5))