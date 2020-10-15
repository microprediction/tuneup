from platypus import NSGAII, Problem, Real, EvolutionaryStrategy, GeneticAlgorithm


def evolutionary_cube(objective,scale,n_trials,n_dim,with_count=False):
    return platypus_cube(objective=objective,scale=scale,n_trials=n_trials,n_dim=n_dim,with_count=with_count,strategy=EvolutionaryStrategy)

def genetic_cube(objective,scale,n_trials,n_dim,with_count=False):
    return platypus_cube(objective=objective,scale=scale,n_trials=n_trials,n_dim=n_dim,with_count=with_count,strategy=GeneticAlgorithm)


def platypus_cube(objective,scale, n_trials, n_dim, strategy, with_count=False):

    global feval_count
    feval_count = 0

    def _objective(vars):
        global feval_count
        feval_count += 1
        return objective(list(vars))[0]

    problem = Problem(n_dim, 1, 0)
    problem.types[:] = [Real(-scale, scale)]*n_dim
    problem.constraints[:] = "<=0"
    problem.function = _objective

    algorithm = strategy(problem)
    algorithm.run(n_trials)
    feasible_solution_obj = [s.objectives[0] for s in algorithm.result if s.feasible]
    best_obj = min(feasible_solution_obj)
    return (best_obj, feval_count) if with_count else best_obj

if __name__ == '__main__':
    from tuneup.trivariateobjectives.trivariateboxobjectives import OBJECTIVES

    for objective, scale in OBJECTIVES.items():
        print(evolutionary_cube(objective, scale, n_trials=300, n_dim=6, with_count=True))
        print(genetic_cube(objective, scale, n_trials=120, n_dim=6, with_count=True))
