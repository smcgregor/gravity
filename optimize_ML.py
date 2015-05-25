from FireGirlOptimizer import *
import os

def optimize_ML(starting_policy, objective_fn="J3"):
    """This function repeats short gradient decents until new pathways need to be generated.



    """
    
    #Load the two pathway sets
    print("Loading training and holdout sets...")
    holdout_set = load_pathway_set("ML_holdout_set")
    training_set = load_training_set("ML_training_set")

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

    ML_pol = load_policy("starting_pol.policy","ML_training_set")

    print("Creating optimizer objects and normalizing feature values...")
    #create a FireGirlPolicyOptimizer object and load up the info it needs
    opt = FireGirlPolicyOptimizer()
    opt.pathway_set = training_set
    opt.normalizeAllFeatures()
    opt.setPolicy(ML_pol)
    #because we never called opt.createFireGirlPathways, the initial "generation weights" were never calculated, so do it here
    opt.calcPathwayWeights()
    opt.setObjFn(objective_fn)

    #create a second optimizer object 
    opt_holdout = FireGirlPolicyOptimizer()
    opt_holdout.pathway_set = training_set
    opt_holdout.normalizeAllFeatures()
    opt_holdout.setPolicy(ML_pol)
    #because we never called opt.createFireGirlPathways, the initial "generation weights" were never calculated, so do it here
    opt_holdout.calcPathwayWeights()
    opt_holdout.setObjFn(objective_fn)
    
    #Get the current values against the given policy
    best_holdout_val = opt_holdout.calcObjFn()
    best_opt_val = opt.calcObjFn()
    
    #how many gradient decent steps to allow?
    descent_steps = 2
    
    print("Initial training set obj.fn. val: " + str(round(best_opt_val)) )
    print("Initial holdout set obj.fn. val:  " + str(round(best_holdout_val)) )
    
    #Begining Machine Learning Loop
    print("Beginning ML loop...")
    while True:
        #checking failsafe, to avoid infinite loops
        iter_count += 1
        if iter_count > fail_safe_count:
            print("optimize_ML() has reached its failsafe limit on iterations, and is exiting")
            break
        
        print("  l-bfgs-b pass #" + str(iter_count))
        opt_result = opt.optimizePolicy(descent_steps)

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

    #print final values
    print("Final training set obj.fn. val: " + str(round(best_opt_val)) )
    print("Final holdout set obj.fn. val:  " + str(round(best_holdout_val)) )



def load_pathway_set(self,subfolder):
    """Loads a saved set of pathways from current_directory/subfolder
    """
    
    pathway_set = []
    
    #look at every *.pathways file in the training set folder
    for f in os.listdir(os.getcwd() + os.sep + subfolder):
        if f.endswith(".pathways"): 
            pkl_file = open(f, 'rb')
            this_set = pickle.load(pkl_file)
            pkl_file.close()
            
            #force each pathway to update their values
            for pw in this_set:
                pw.updateNetValue()
                
            #and add these to the training set
            pathway_set = pathway_set + this_set           
                
    return pathway_set


def load_policy(self, filename, subfolder=None):
    """Loads a policy from the given folder"""
    f_name = os.getcwd() + os.sep
    if not subfolder == None:
        f_name = f_name + subfolder + os.sep + filename
    else:
        f_name = f_name + filename
        
    pkl_file = open(f_name, 'rb')
    pol = pickle.load(pkl_file)
    pkl_file.close()
    
    return pol
    


