from FireGirlOptimizer import *

def optimize_ML(self, starting_policy, objective_fn="J3"):
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


    #create a FireGirlPolicyOptimizer object and load up the info it needs
    opt = FireGirlPolicyOptimizer()
    opt.pathway_set = training_set
    opt.setPolicy(ML_pol)
    opt.setObjFn("J3")

    #create a second optimizer object 
    opt_holdout = FireGirlPolicyOptimizer()
    opt_holdout.pathway_set = training_set
    opt.setObjFn("J3")


    #Begining Machine Learning Loop
    while True:
        #checking failsafe, to avoid infinite loops
        iter_count += 1
        if iter_count > fail_safe_count:
            print("optimize_ML() has reached its failsafe limit on iterations, and is exiting")
            break


        opt_result = opt.optimizePolicy(iter_count)

        #TODO once opt.optimizePolicy() has a new return value structure, update code below:
        #pulling out individual results
        opt_result_b = opt_result[0][1]
        opt_result_val = opt_result[1][1]
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


