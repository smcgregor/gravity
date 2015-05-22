
def optimize_ML(self, objfn, fprime, starting_policy):
    """This function repeats short gradient decents until new pathways need to be generated.



    """
    
    #Load the two pathway sets
    holdout_set = self.load_holdout_set()
    training_set = self.load_training_set()

    #when evaluating each new policy against the holdout set, some dissimprovement can be allowed
    #this amount will be added (a disimprovement) to the previous best value. New values must fall
    #below the sum, or else the policy will be considered invalid against the holdout set.
    holdout_wiggle = 0

    #flags
    opt_fail = False
    holdout_fail = False

    #failsafe counter: ML loop will exit if it goes around this many times, irregardless of improvements
    fail_safe_count = 1000

    #iterations need to be counted
    iter_count = 0

    ML_pol = self.load_policy()

    #This is a minimization routine, so high values are bad
    best_holdout_val = objfn(holdout_set)
    best_opt_val = 99999999999


    #Begining Machine Learning Loop
    while True:
        #checking failsafe, to avoid infinite loops
        iter_count += 1
        if iter_count > fail_safe_count:
            print("optimize_ML() has reached its failsafe limit on iterations, and is exiting")
            break



        #scipy gradient descent method
        #signature is:
        #scipy.optimize.fmin_l_bfgs_b(func, x0, fprime=None, args=(), approx_grad=0, bounds=None, m=10, 
        #                             factr=10000000.0, pgtol=1e-05, epsilon=1e-08, iprint=-1, maxfun=15000,
        #                             maxiter=15000, disp=None, callback=None)
        # func is a function name, at is referenceing the objective function that it will use
        # x0 is the starting parameters that fmin_l_bfgs_b() will use
        # fprime="None" is telling fmin...() that we are not passing in a function to calculate derivitave values
        # args=() is asking for any input arguments needed for the objective function, other than the beta parameters
        # approx_grad is telling fmin...() to approximate it's own derivatives, or to use some other gradient
        # bounds should be a list of upper and lower bound pairs. See scipy.optimize.fmin_l_bfgs_b documentation.
        # m is the maximum number of variable metric corrections used to define the limited memory matrix. 
        #     (The limited memory BFGS method does not store the full hessian but uses this many terms in an 
        #      approximation to it.)
        # factr is the iteration stopping point. When (f^k - f^{k+1})/max{|f^k|,|f^{k+1}|,1} <= factr * eps, where eps 
        #      is the machine precision, which is automatically generated by the code. Typical values for factr are: 
        #      1e12 for low accuracy; 1e7 for moderate accuracy; 10.0 for extremely high accuracy.
        # The rest of the arguments are left as defaults.

        x0 = scipy.array(starting_policy.getParams())

        #setting up bounds, starting with the constant
        b_bounds = [[-10000.0,10000.0]]
        for i in range(len(x0) - 1):
            b_bounds.append([-10.0,10.0])

        #setting max iterations per run through the gradient descent method
        iter_cap = 100

        opt_result = scipy.optimize.fmin_l_bfgs_b(objfn, 
                                                  x0,
                                                  fprime,
                                                  args=[training_set, ML_pol], 
                                                  approx_grad=False,
                                                  bounds=b_bounds,
                                                  factr=1,
                                                  maxiter=iter_cap)

        #pulling out individual results
        opt_result_b = opt_result[0]
        opt_result_val = opt_result[1]
        opt_result_dict = opt_result[2]


        #checking for improvements gained by this policy
        if opt_result_val <= best_opt_val:
            #improvement was found, so record it
            best_opt_val = opt_result_val
        else:
            #no improvement was found, so exit the loop
            opt_fail = True

        #checking for improvements gained against the holdout set
        if objfn(holdout_set, ML_pol) <= best_holdout_val + holdout_wiggle:
            #improvement was found, so record it
            best_holdout_val = objfn(holdout_set, ML_pol)
        else:
            #no improvement was found, so exit the loop
            holdout_fail = True

        #if improvements were found in BOTH the training AND the holdout set, record the new policy and continue
        if (not opt_fail) and (not holdout_fail):
            #improvements in both, so record the policy for the next iteration
            ML_pol.setParams(opt_result_b)
        else:
            #one of the two failed, so exit the loop
            break


    #Machine Learning Loop has exited

    if opt_fail:
        print("scipy.optimize.fmin_l_bfgs_b has found a local optima")

    if holdout_fail:
        print("the final policy did not improve the expectation on the holdout set")






def load_holdout_set(self):
    pass

def load_training_set(self):
    pass

def load_policy(self):
    pass

