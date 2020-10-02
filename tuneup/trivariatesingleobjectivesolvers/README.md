
Solvers that work on box domains ... here 3-dim

To make horse race simple, each is like this:

    cube(objective,scale, n_trials):
        """
           Return lowest objective function found in 
           the cube [-scale,scale]^3 after n_trials
           as a 1-tuple
        """
        
Don't ask why it should return a 1-tuple 