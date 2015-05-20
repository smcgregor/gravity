from FireGirlPathway import *
from FireGirlPolicy import *
import math, scipy, pickle
from scipy.optimize import *

class FireGirlPolicyOptimizer:
    def __init__(self, USING_FIREGIRL_PATHWAYS=True):
        #A list to hold all the pathways in a data set, whether they represent FireGirl or
        #    FireWoman pathways
        self.pathway_set = []
        
        #A list to hold the net values of each pathway in the data set
        self.pathway_net_values =[]
        
        #A list to hold the "probability weights" of each pathway
        self.pathway_weights = []                       #J1 weights
        self.pathway_weights_normalized = []            #J1.1 weights
        self.pathway_weights_averaged = []              #J2 weights
        self.pathway_weights_importance_sampling = []   #J3 weights
        self.pathway_weights_generation = []   #denominators for J3 weights

        
        #Boundaries for what the parameters can be set to during scipy's optimization routine:
        self.b_bounds = []

        if USING_FIREGIRL_PATHWAYS == True:
            for i in range(11):
                self.b_bounds.append([-10.0,10.0])
        else:
            #set FireWoman bounds appropriately
            pass
        #and set the constant to be able to vary more freely
        self.b_bounds[0] = [-1000.0, 1000.0]


        #Flag: Use log(probabilities)  -  If we want to force sums of log(probs), set to True
        #                                 To just multiply probabilities, set to False
        self.USE_LOG_PROB = False
        
        #Flag: use normalized weights for the objective function
        self.NORMALIZED_WEIGHTS_OBJ_FN = False
        #Flag: use normalized weights for F prime
        self.NORMALIZED_WEIGHTS_F_PRIME = False
        #Flag: use averaged weights for the objective function
        self.AVERAGED_WEIGHTS_OBJ_FN = False
        #Flag: use averaged weights for F prime
        self.AVERAGED_WEIGHTS_F_PRIME = False

        #Flag: Use importance sampling weights (J3)
        self.IMPORTANCE_SAMPLING = True


        #Flag: Suppress all outputs that originate from this object
        self.SILENT = False
        #Flag: Suppress all outputs that originate from pathways this object creates/uses
        self.MUTE_PATHWAYS = True

        #Flag: Should Pathways remember their state histories
        self.PATHWAYS_RECORD_HISTORIES = False

        #Flag: Custom Model Parameters. If the optimizer has recieved custom model parameters,
        # this flag warns createFireGirlPathways, and the parameters are assigned appropriately
        self.CUSTOM_MODEL_PARAMETERS = False
        self.custom_transition_params = {}
        self.custom_reward_params = {}
        

        #Flag: Using FireGirl pathways = True
        #      Using FireWoman pathways = False
        self.USING_FIREGIRL_PATHWAYS = USING_FIREGIRL_PATHWAYS


        #The policy that is controlling each pathway's fire suppression choices
        #This should be set to one of the two child classes of HKBFire_Policy: 
        #  FireGirl_Policy or FireWoman_Policy

        if USING_FIREGIRL_PATHWAYS == True:
            #FireGirl uses 11 parameters, so set them all to 0 (coin-toss policy)
            self.Policy = FireGirlPolicy(None,0.0,11)
        else:
            #FireWoman uses ??? parametres, so set them all to 0 (coin-toss policy)
            self.Policy = FireGirlPolicy(None,0.0,30)


        ##########################################################################################
        #FireGirl-specific flags and data members. These are unused if FireWoman-style pathways
        #    are being used
        ##########################################################################################

        #A flag for whether or not to include ending pathways' standing timber
        #   value in the total pathway value
        self.count_standing_timber = False
      


    ##########################
    # Optimization Functions #
    ##########################

    def normalizeAllFeatures(self, rng=5.0):
        #This function normalizes each feature of each ignition in each pathway to fall
        #  between its rng and -rng arguments. It will also store each ignition's 
        #  original features in the ignition.features_raw[] array.

        #arrays to hold the max and min of each feature over ALL ignitions in ALL pathways
        feature_max = []
        feature_min = []

        #fill the max and min lists with placeholder values
        for i in range(len(self.pathway_set[0].ignition_events[0].features)):
            feature_max.append( -999999999.9 )
            feature_min.append(  999999999.9 )

        #re-initialize ignition.feature_raw arrays
        for pw in self.pathway_set:
            for ig in pw.ignition_events:
                ig.features_raw = []


        #look in every pathway
        for pw in self.pathway_set:
            #look in every ignition in this pathway
            for ig in pw.ignition_events:
                #look at each feature in this ignition
                for f in range(len(ig.features)):

                    #if this feature is higher than the previously found max, remember it
                    if ig.features[f] > feature_max[f]:
                        feature_max[f] = ig.features[f]
                    #if this feature is lower than the previously found min, remember it
                    if ig.features[f] < feature_min[f]:
                        feature_min[f] = ig.features[f]

        #calculate means
        feature_mean = []
        for f in range(len(feature_max)):
            feature_mean.append(   (feature_max[f] + feature_min[f]) / 2.0   )

        #calculate normalization magnitude
        #this is the value that we'll divide each feature by, once its been recentered around
        # a mean of zero
        feature_norm_mag = []
        for f in range(len(feature_max)):
            feature_norm_mag.append(  (feature_max[f] - feature_mean[f]) / rng )
        if not self.SILENT:
            #print(str(feature_norm_mag))
            pass

        #now normalize each feature value to fall between "max" and "min"
        #in every pathway
        for pw in self.pathway_set:
            #in every ignition in this pathway
            for ig in pw.ignition_events:
                #look at each feature in this ignition
                for f in range(len(ig.features)):
                    #we forced a re-initialization of of the ignition.features_raw lists, so 
                    # we have to append new items to it for each feature to save them
                    ig.features_raw.append(ig.features[f])

                    #normalize step 1: shift the mean to zero
                    ig.features[f] -= feature_mean[f]

                    #normalize step 2: change magnitude to be within +/- rng
                    #but check for 0's:  Any feature that is absolutely constant (like the constant) will 
                    # have a feature_norm_mag value of zero. When that's the case, just set the feature
                    # to one (rather than zero, because a one will allow the constant parameter to actually
                    #     do something)
                    if feature_norm_mag[f] == 0:
                        ig.features[f] = 1.0
                    else:
                        ig.features[f] = ig.features[f] / feature_norm_mag[f]

        #if desired, print the max, min, mean, and norm values
        if not self.SILENT:
            print("Feature Descriptions before normalization")
            print("Max values:")
            print(str(feature_max))
            print("Ave values:")
            print(str(feature_mean))
            print("Min values:")
            print(str(feature_min))
            print("Normalization Magnitude:")
            print(str(feature_norm_mag))

    def calcPathwayWeights(self, USE_SELF_POLICY=True):
        #This function looks through each fire of a given pathway and applies the current
        #  policy to the features of each one. The resulting 'probability' from the policy 
        #  function is either multiplied or 'log-summed' be the others to produce the final 
        #  weighting value. This is done for every pathway in the pathway_set, and each
        #  weight is assigned to pathway_weights[] at the same index as their pathway in 
        #  the pathway_set list

        #clearing old weights
        self.pathway_weights = []                       #J1 weights
        self.pathway_weights_normalized = []            #J1.1 weights
        self.pathway_weights_averaged = []              #J2 weights
        self.pathway_weights_importance_sampling = []   #J3 weights

        #iterating over each pathway and appending each new weigh to the list
        for pw in self.pathway_set:

            #setting the pathway's USE_LOG_PROB flag to match the optimizer's flag
            pw.USE_LOG_PROB = self.USE_LOG_PROB
        
            #setting this pathway's policy to the current one
            if USE_SELF_POLICY:
                pw.assignPolicy(self.Policy)
            else:
                #setting this to false indicates that the pathways have their own policies
                # (possibly applied elsewhere) and that they should use them, instead of
                # taking the optimizer's current policy. Mostly used for testing
                pass
            
            #calculate all three weighting regimes
            p1 = pw.calcTotalProb()             #J1 weights - "joint probability"
            p2 = pw.calcAveProb()               #J2 weights - averaged probabilities
            
                
                
            # # pw.DEBUG = True
            # p = 0.0
            # if self.USE_AVE_PROB:
                # # TESTING - USING Average Probability instead of total probability
                # p = pw.calcAveProb()
            # # pw.DEBUG = False
            # else:
                # p = pw.calcTotalProb()
            
            
            # # Doing J1.1 probability normalization step
            # if self.USE_NORMALIZATION:
                # p = p / pw.calcSumOfProbs()
           
            self.pathway_weights.append(p1)                  #J1 weights
            self.pathway_weights_averaged.append(p2)         #J2 weights
        
                    
        #calculate sum of ALL weights
        weight_sum = 0.0
        for w in self.pathway_weights:
            weight_sum += w
        
        #computing normalization of each pathway weight over the sum of ALL pathway weights
        pathway_weights_normalized = []
        for w in self.pathway_weights:
            self.pathway_weights_normalized.append( w / weight_sum )  #J1.1 weights

        #calculating J3 weights
        #but first see if any generation weights have been assigned. If this function is 
        #  being called from createFireGirlPathways(), self.pathway_weights_generation will 
        #  not have been instantiated yet, and this function is being called precisely to 
        #  do just that. So, if that's the case, we also don't have to worry about calculating
        #  the J3 weights because that will happen in optimizePolicy() and elsewhere
        if len(self.pathway_weights_generation) > 0:
            for i in range(len(self.pathway_weights)):
                #checking for very low values:
                #if self.pathway_weights_generation[i] < 0.0001: self.pathway_weights_generation[i] = 0.0001

                #assigning weights
                self.pathway_weights_importance_sampling.append(self.pathway_weights[i] / self.pathway_weights_generation[i])
                    
    def calcObjFn(self, b=None):
        #This function contains the optimization objective function. It operates
        #  on the current list of pathways. If any values for 'b' are passed in,
        #  (most likely by scipy.optimize.fmin_l_bfgs_b(), then they are assigned
        #  to the current HKBFire_Policy object so that subsequent function calls
        #  will use the correct ones.
                
        #The objective function is the sum of each pathway's net value, weighted
        #  by the overall probability of its suppression choices. This probabilty
        #  is simply the suppression decision values from the logistic function
        #  all multiplied together.


        #variable to hold the final value
        obj_fn_val = 0    
        
        # checking for new beta parameters
        if not b == None:
            self.Policy.setParams(b)

        #Note: self.calcPathwayWeights will assign this policy to each pathway

        # Calculate the weights... these will use the current Policy
        #    rather than whatever policy the pathways used during simulation
        #    Typically, this will be the multiplied total of the inidividual probabilities
        #    associated with following or not-following the policy
        
        self.calcPathwayWeights()
        
        #Note: self.pathway_net_values is being assigned either in:
        #   1) createFireGirlPathways() when those pathways are first made
        #   2) loadFireGirlPathways() when those pathways are loaded up
        #   3) loadFireWomanPathways() when those pathways are loaded up

        #now assign them to the local list, for ease
        self.pathway_net_values = []
        for pw in self.pathway_set:
            self.pathway_net_values.append(pw.net_value)
        
        #a variable to hold the sum of ALL the probability-weighted pathway values
        total_value = 0
        
        #loop over all the values/weights and sum them
        for pw in range(len(self.pathway_set)):
        
            #check which weights to use:
            #Importance Sampling (J3) supercedes Normalization (J1.1)
            if self.IMPORTANCE_SAMPLING:
                #using J3 weights
                #TODO: Verfiy that this is how to do this???
                total_value += self.pathway_net_values[pw] * self.pathway_weights_importance_sampling[pw]

            #Normalization (J1.1) supercedes averaging (J2)
            elif self.NORMALIZED_WEIGHTS_OBJ_FN:
                #using J1.1 normalized weights
                total_value += self.pathway_net_values[pw] * self.pathway_weights_normalized[pw]
            else:
                #using "un-normalized" weights... check averaging...
                if self.AVERAGED_WEIGHTS_OBJ_FN:
                    #using J2 averaged weights
                    total_value += self.pathway_net_values[pw] * self.pathway_weights_averaged[pw]
                else:
                    #using straight J1.0 "joint probability weights"
                    total_value += self.pathway_net_values[pw] * self.pathway_weights[pw]
            
        


        #NOTE:
        #any final checks/modifications to total_val can go here:

        #since scipy fmin... is a minimization routine, return the negative
        obj_fn_val = -1.0 * total_value    
        
        
        return obj_fn_val

    def FP_prob(self, pw, ign):
        #return the probability that the current policy predicts for a specific ignition of a specific pathway
       
        #NOTE: the individual pathways have already had their policies updated
        #  to the current one in self.calcPathwayWeights()

        #get the suppression choice of this pathway at this ignition
        choice = self.pathway_set[pw].getChoice(ign)
        #and set it to binary
        sup = 0
        if choice == True: sup = 1

        #get the new probability (according to the current policy) of suppressing
        # this ignition in this pathway
        prob_pol = self.pathway_set[pw].getProb(ign)

        #set the probability of actually doing what we did
        prob = sup * prob_pol   +   (1-sup)*(1-prob_pol) 
        
        #checking for unreasonably small probabilities
        if prob == 0:
            prob = 0.00001

        return prob
        
    def FP_delta_prob(self, beta, pw, ign, prob):
        #this function calculates the inner "delta_prob" value for each calculation of the derivitive.
        # caclObjFPrime() loops over it repeatedly, and passes in which parameter (beta), pathway (pw) and
        # ignition (ign) to calculate value, which is then summed in caclObjFPrime()
        
        #get the suppression choice of this pathway at this ignition
        choice = self.pathway_set[pw].getChoice(ign)
        #and set it to binary
        sup = 0
        if choice == True: sup = 1
        
        #get the cross product of this pathway at this ignition
        cross_product = self.pathway_set[pw].getCrossProduct(ign)

        #get the feature of this pathway and this ignition for this beta
        flik = self.pathway_set[pw].getFeature(ign, beta)


        delta_lgstc = flik * self.Policy.logistic(cross_product) * (1.0 - self.Policy.logistic(cross_product))

        delta_prob = sup * delta_lgstc + (1 - sup)*(-1)*delta_lgstc
        
        return delta_prob
    
    def calcObjFPrime(self, betas=None):
        #This function returns the gradient of the objective function

        #The scipy documentation describes the fprime arguement as:
        #fprime : callable fprime(x,*args)
        #The gradient of func. If None, then func returns the function value and the 
        #  gradient (f, g = func(x, *args)), unless approx_grad is True in which case func returns only f.

        #The return value should probably just be a list of the derivitive values with respect to each 
        #   b-parameter in the policy

        #  d Obj()/d b_k value is 
        #
        #   Sum over pathways [ val_l * product over ignitions [ prob_i ] * sum over ignitions [d wrt prob / prob] ]
        #
        #   where d wrt prob =  sup_i * d(logistic(b*f)) + (1 - sup_i)(-1) (d(logistic(b*f)))
        #
        #   and where d(logistic(b*f)) = f_l,i,k * logistic(f_l,i,k * b_k) * (1 - logistic(f_l,i,k * b_k))

        #Assign values to b. I don't think this function will ever be called
        #  outside of the l_bfgs function, but if so, handle it:
        b = None
        if betas == None:
            b = self.Policy.getParams()
        else:
            b = betas

        # list to hold the final values, one per parameter
        d_obj_d_bk = []
        for i in range(len(b)):
            d_obj_d_bk.append(0.0)
            
        #get the weight (total or ave) for each pathway decision sequence using the 
        #   current policy (which is possibly being varied by l_bfgs, etc...)
        
        self.calcPathwayWeights()
        
        #iterate over each beta and evaluate the gradient along it
        for beta in range(len(b)):

            #SEE MATHEMATICS DOCUMENTATION FOR A DETAILED EXPLANATION OF ALL THAT FOLLOWS

            #variable to hold the sum of the delta(prob)/prop values
            sum_delta_prob = 0.0
            sum_delta_prob_AVE = 0.0

            for pw in range(len(self.pathway_set)):

                #reset value for this pathway
                sum_delta_prob = 0.0
                sum_delta_prob_AVE = 0.0

                for ign in range(self.pathway_set[pw].getIgnitionCount()):

                    #compute both the current policy's probability at this ignition
                    prob = self.FP_prob(pw, ign)

                    delta_prob = self.FP_delta_prob(beta, pw, ign, prob)

                    sum_delta_prob_AVE += delta_prob #for use in the J2 "averaged" calculation
                    sum_delta_prob += delta_prob / prob #for use in J1 "standard" and J1.1 "normalized"

                
                #finished adding up sum_delta_prob for all the ignitions in this pathway, so
                # calculate the d/dx value:
                
                
                #check which weights to use, and to the derivative appropriately
                if self.IMPORTANCE_SAMPLING:
                    #using J3 Importance Sampling Weights
                    d_obj_d_bk[beta] += self.pathway_net_values[pw] * self.pathway_weights_importance_sampling[pw] * sum_delta_prob
                elif self.NORMALIZED_WEIGHTS_F_PRIME:
                    #using normalized weights inside the derivative calculation (J1.1)
                    d_obj_d_bk[beta] += self.pathway_net_values[pw] * self.pathway_weights_normalized[pw] * sum_delta_prob
                else:
                    if self.AVERAGED_WEIGHTS_F_PRIME:
                        #doing average-weight calculation (J2)
                        invI = (1.0 / self.pathway_set[pw].getIgnitionCount())
                        d_obj_d_bk[beta] += self.pathway_net_values[pw] * invI * sum_delta_prob_AVE                            
                    else:
                        #using standard joint-probability math (J1.0)
                        d_obj_d_bk[beta] += self.pathway_net_values[pw] * self.pathway_weights[pw] * sum_delta_prob
                    
                    

                #going on to the next pathway

            #going on to the next beta

        #finished with all betas

        #because this is a minimization routine, and the objective function is being flipped, so too
        #  should be the derivatives
        for b in range(len(d_obj_d_bk)):
            d_obj_d_bk[b] *= -1.0


        # And Finally, return the list
        return scipy.array(d_obj_d_bk)
   
    def optimizePolicy(self, iterations=1, acceptance_threshold=None):
        #This function will work through the given number of gradient descent 
        #  iterations using the current set of pathways for its data set.
        #It returns a list containing two elements
        #  -The first is a list of the policy parameters used in
        #  each iteration
        #  -The second is a list of the optimized objective function value 
        #  for each iteration

        
        # a list to hold each iteration's final objective function value
        obj_vals = []
        # a list to hold the parameters returned by each iteration
        param_sets = []
        
        #record the first 'optimization value' which is really just a placeholder 
        #  to keep indices even
        obj_vals.append(self.calcObjFn())
        #record the first parameter set
        param_sets.append(self.Policy.getParams())
        
        for iter in range(iterations):
            #tell scipy to optimize our objective function (calcObjectiveFn())
            #  given a certain set of parameters...
            
            #running the scipy gradient descent method
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
            

            #setting x0 to the initial guess, which can just be whatever our current policy parameters are.
            #converting to numpy arrays

            #checking to see if the policy actually has parameters yet
            x0 = []
            if len(self.Policy.getParams()) == 0:
                #the Policy object's parameter array is empty, so lets arbitrarily fill it
                if self.USING_FIREGIRL_PATHWAYS:
                    self.Policy.setParams([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
                else:
                    #this is a FireWoman pathway/policy, so fill it accordingly...
                    pass
            x0 = scipy.array(self.Policy.getParams())

            #DEBUG
            if not (len(self.b_bounds) == len(x0)):
                print("error in FireGirlOptimizer.optimizePolicy...")
                print("x0 = " + str(x0))
                print("bounds = " + str(self.b_bounds))



            #               arg names:    func            x0  fprime,               args, approx_grad, bounds       ,  m, factr
            output_policy = fmin_l_bfgs_b(self.calcObjFn, x0, self.calcObjFPrime,   [],   False,       self.b_bounds,  10, 1)
            
            #the output of fmin_l_bfgs_b() has the following structure: [x, f, d], where:
            #   x : array_like
            #       Estimated position of the minimum.
            #   f : float
            #       Value of func at the minimum.
            #   d : dict
            #       Information dictionary.
            
            
            #record the new parameter set
            param_sets.append(output_policy[0])
            
            #record the final objective function value
            obj_vals.append(output_policy[1])
            
            
          
            #take the new parameter set and assign them back to the policy
            #for i in range(len(output_policy[0])):
            #    self.Policy.b[i] = output_policy[0][i] + 1.0 - 1.0
            self.Policy.setParams(output_policy[0])

            #self.Policy.b = output_policy[0]
            
            #debugging check
            #print("output policy is: " + str(output_policy[0]))
            #print("after assigning it to self.Policy.b, ...b is: ")
            #print(str(self.Policy.b))
            
            #run the next iteration
            
            
        #Iterations are Finished, so prepare the return value
        ret_val = [param_sets, obj_vals]
        
        return ret_val
    
    def setObjFn(self, objfn):
        """Sets the optimizer's flags to set it up for the given objective function type.

        Arguements
        objfn: a string indicating which objective function to use.
        --options are:
        -- "J1" for the J1.1 objective function (original joint-probability method with normalization)
        -- "J2" for the J2 objective function (Hailey's averaging method)
        -- (J1.0 is ineffective, so it is not represented here)
        """

        if objfn == "J1":
            #set flags for J1.1
            self.IMPORTANCE_SAMPLING = False
            self.NORMALIZED_WEIGHTS_OBJ_FN = True
            self.NORMALIZED_WEIGHTS_F_PRIME = True
            self.AVERAGED_WEIGHTS_OBJ_FN = False
            self.AVERAGED_WEIGHTS_F_PRIME = False
        elif objfn == "J2":
            #set flags for J2
            self.IMPORTANCE_SAMPLING = False
            self.NORMALIZED_WEIGHTS_OBJ_FN = False
            self.NORMALIZED_WEIGHTS_F_PRIME = False
            self.AVERAGED_WEIGHTS_OBJ_FN = True
            self.AVERAGED_WEIGHTS_F_PRIME = True
        elif objfn == "J3":
            self.IMPORTANCE_SAMPLING = True
            self.NORMALIZED_WEIGHTS_OBJ_FN = False
            self.NORMALIZED_WEIGHTS_F_PRIME = False
            self.AVERAGED_WEIGHTS_OBJ_FN = False
            self.AVERAGED_WEIGHTS_F_PRIME = False

        else:
            #undefined behavior... default to J1.10
            print("Undefined objective function: " + str(objfn) + "   Setting J1.0 by default")
            self.IMPORTANCE_SAMPLING = False
            self.NORMALIZED_WEIGHTS_OBJ_FN = False
            self.NORMALIZED_WEIGHTS_F_PRIME = False
            self.AVERAGED_WEIGHTS_OBJ_FN = False
            self.AVERAGED_WEIGHTS_F_PRIME = False

    def printOptOutput(self, output):
        #takes the outputs from the optimize() function and prints them in a nicer way
        params = output[0]
        obj_vals = output[1]
        
        print("         ObjFn Val,     Params.....")
        print("                        CONS   date    date2    temp   wind   timb   timb8  timb24  fuel  fuel8  fuel24")
        for v in range(len(obj_vals)):
            if v == 0:
                print("before: "),
            else:
                print("after:  "),
            print(str(round(obj_vals[v],10)) + "  "),
            
            for p in range(len(params[v])):
                print(" " + str(round(params[v][p],5))),
            
            print("") #to end the line
                
            
            
    
    ###############################
    # FireGirl-specific Functions #
    ###############################

    def setFireGirlModelParameters(self,transition_dictionary,reward_dictionary):
        """Takes two dictionaries containing model parameters. Subsequent pathways will use these values.

        Arguemnts have the following key:value pairs

        reward =  {"Discount": 1,
                    "Suppression Fixed Cost": 500, 
                    "Suppression Variable Cost": 500
                   }
                        
        transition = { "Harvest Percent": 0.95,
                        "Minimum Timber Value": 50,
                        "Slash Remaning": 10,
                        "Fuel Accumulation": 2,
                        "Suppression Effect": 0.5
                      }
        """

        self.CUSTOM_MODEL_PARAMETERS = True
        self.custom_reward_params = reward_dictionary
        self.custom_transition_params = transition_dictionary
    
    def clearFireGirlModelParameters(self):
        self.CUSTOM_MODEL_PARAMETERS = False
        self.custom_transition_params = {}
        self.custom_reward_params = {}

    def updatePathwayCustomParameters(self):
        """ Uses stored model parameter dictionaries and assigns them to the current pathway set

        Dictionaries should have...

        reward =  {"Discount": 1,
                "Suppression Fixed Cost": 500, 
                "Suppression Variable Cost": 500
               }
                    
        transition = { "Harvest Percent": 0.95,
                    "Minimum Timber Value": 50,
                    "Slash Remaning": 10,
                    "Fuel Accumulation": 2,
                    "Suppression Effect": 0.5
                  }
        """

        #reward parameters

        if "Discount" in self.custom_reward_params.keys():
            for pw in self.pathway_set:
                #TODO: Add Pathway discount rate. =)
                pass

        if "Suppression Fixed Cost" in self.custom_reward_params.keys():
            for pw in self.pathway_set:
                pw.fire_suppression_cost_per_day = self.custom_reward_params["Suppression Fixed Cost"]

        if "Suppression Variable Cost" in self.custom_reward_params.keys():
            for pw in self.pathway_set:
                pw.fire_suppression_cost_per_cell = self.custom_reward_params["Suppression Variable Cost"]


        #state transition parameters

        if "Harvest Percent" in self.custom_transition_params.keys():
            for pw in self.pathway_set:
                pw.logging_percentOfIncrement = self.custom_transition_params["Harvest Percent"]

        if "Minimum Timber Value" in self.custom_transition_params.keys():
            for pw in self.pathway_set:
                pw.logging_min_value = self.custom_transition_params["Minimum Timber Value"]

        if "Slash Remaning" in self.custom_transition_params.keys():
            for pw in self.pathway_set:
                pw.logging_slash_remaining = self.custom_transition_params["Slash Remaning"]

        if "Fuel Accumulation" in self.custom_transition_params.keys():
            for pw in self.pathway_set:
                pw.growth_fuel_accumulation = self.custom_transition_params["Fuel Accumulation"]
            
        if "Suppression Effect" in self.custom_transition_params.keys():
            for pw in self.pathway_set:
                pw.fire_suppression_rate = self.custom_transition_params["Suppression Effect"]

        if "Growth Model" in self.custom_transition_params.keys():
            for pw in self.pathway_set:
                pw.setGrowthModel(self.custom_transition_params["Growth Model"])

        if "Use Original Bugs" in self.custom_transition_params.keys():
            for pw in self.pathway_set:
                if self.custom_transition_params["Use Original Bugs"] == 0:
                    pw.USE_BUGS = True
                else:
                    pw.USE_BUGS = False

        if "Landscape Size" in self.custom_transition_params.keys():
            for pw in self.pathway_set:
                pw.setLandscapeSize(int(self.custom_transition_params["Growth Model"]))

    def createFireGirlPathways(self, pathway_count, years, start_at_ID=0, policy=None):
        #This function creates a new set of FireGirl-style pathways (deleting all current
        #    pathway data)
        
        #Check if we need a new policy, or if one was passed in
        if policy == None:
            #INSTEAD of what is below, just let the current policy stand. It should never
            #      be null, because a coin-toss policy gets created at obj. instantiation
            #no policy passed, so create a new one
            #self.Policy = FireGirlPolicy(None,0,11)
            pass
            
        else:
            #one was passed, so set it to the current one.
            self.Policy = policy
        
        #Clear the pathway_set list in case there's old pathways in it
        self.pathway_set = []
        
        #Create new pathways and add them to the pathway_set list
        for i in range(start_at_ID, start_at_ID + pathway_count):
            self.pathway_set.append(FireGirlPathway(i, self.Policy))

        #Check for custom model parameters, and if found, set them in each pathway
        if self.CUSTOM_MODEL_PARAMETERS:
            #custom parameters have been given, so parse them and assign them
            self.updatePathwayCustomParameters()
                
       
        #Have each pathway create new data for itself. Right now their timber_values 
        #   and fuel_loads are set uniformally to zero
        if not self.SILENT:
            if pathway_count == 1:
                print("Creating pathway " + str(start_at_ID))
            else:
                print("Creating pathways " + str(start_at_ID) + "-" + str(start_at_ID + pathway_count))

        for pw in self.pathway_set:

            #Silence the pathways, if this object is set to silent
            if self.SILENT or self.MUTE_PATHWAYS:
                pw.SILENT = True

            if self.PATHWAYS_RECORD_HISTORIES:
                pw.SAVE_HISTORY = True
            else:
                pw.SAVE_HISTORY = False
            
            #have each pathway create timber/fuel data for itself
            pw.generateNewLandscape()

            #Have each pathway simulate for the given number of years
            pw.doYears(years)

            #and after all years are finished, have each pathway calculate its net value
            #this is being handled by the pathway objects now
            #pw.updateNetValue()

        #calculate and save current joint-probability weights
        # these are needed for J3 calculation
        #but firest make sure that there are actual years. In some tests, pathways are created with NO years/events
        if years > 0:
            self.calcPathwayWeights()

        #clear any old values
        self.pathway_weights_generation = []

        #copy values:
        for w in self.pathway_weights:
            self.pathway_weights_generation.append(w + 1.0 - 1.0)
        
 
    ###################
    # Other Functions #
    ###################

    def getNetValues(self):
        """returns a copy of the current list of pathway net values
        """

        #clear the current list
        self.pathway_net_values = []

        #create a copy to return (to force vals, rather than references)
        copy_vals = []

        #have all pathways update their own net values
        for pw in self.pathway_set:
            #updating the official list, while we're here
            self.pathway_net_values.append(pw.updateNetValue())
            #building the return list
            copy_vals.append(pw.updateNetValue())

        return copy_vals

    def saveFireGirlPathways(self, filename):
        output = open(filename, 'wb')

        # Pickle dictionary using default protocol 0.
        pickle.dump(self.pathway_set, output)

        output.close()

    def loadFireGirlPathways(self, filename):
        #This function loads a saved set of FireGirl pathways

        pkl_file = open(filename, 'rb')

        self.pathway_set = []
        self.pathway_set = pickle.load(pkl_file)

        pkl_file.close()

        #and do the post-processing
        
        #force each pathway to update their values
        for ls in self.pathway_set:
            ls.updateNetValue()

    def loadFireWomanPathways(self, filename):
        #This function loads a saved set of FireWoman Pathways

        #REMINDER: this function needs to assign values to self.pathway_net_values

        pass

    def setPolicy(self, policy):
        #take the policy given and give it to every pathway in the current set.
        self.Policy = policy
        for ls in self.pathway_set:
            ls.assignPolicy(self.Policy)

    def resetPolicy(self):
        #This function resets the policy to a 50/50 coin-toss
        self.Policy = FireGirlPolicy(None,0,11)

    def loadPolicy(self, filename):
        #This function loads a saved policy and assigns it to this optimization object
        pass
    