
Solvers that work on box domains ... here 3-dim

Will deprecate soon

To make horse race simple, each is like this:

    cube(objective,scale, n_trials):
        """
           Return lowest objective function found in 
           the cube [-scale,scale]^3 after n_trials
           as a 1-tuple
        """
        
Returning a 1-tuple keeps the multi-objective case alive. 