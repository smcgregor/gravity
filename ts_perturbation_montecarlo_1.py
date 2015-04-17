# I don’t think this is quite what we want. Here is the experiment I would like to see:

# 1.  Generate an initial set of trajectories. Apply your optimization code to find a (locally) optimal policy. Call it pi0

# 2.  Call MonteCarloPolicyEvaluation(pi0)

# 3.  Generate a few perturbations of the policy. If there are m parameters, then I suggest creating 2m perturbed policies. For each policy, you will perturb the mth parameter by +50% and –50% of its learned value, for example. This will give us pi_1 through pi_2m

# 4.  For each policy pi in pi_1, ..., pi_2m call MonteCarloPolicyEvaluation(pi)

# 5.  Compare the values returned by the policy evaluations

# The subroutine MonteCarloPolicyEvaluation(pi) does the following:

# N = 100
# totalReward = 0
# for iter = 1 to N do
#    generate a trajectory of length 50 in which the actions are chosen according to pi
#    let tr = total reward along that trajectory
#    totalReward = totalReward + tr
# end for
# averageReward = totalReward/100
# ## Probably better would be to create a list of the tr values, but I’ll leave that to you
# return averageReward
 
# If pi0 is at a local optimum, then the result of MonteCarloPolicyEvaluation(pi0) should be better than the results of all of the other calls to MonteCarloPolicyEvaluation

# This is just an experimental test for a local optimum.

# --Tom





import random, math
from FireGirlOptimizer import *
FGPO = FireGirlPolicyOptimizer()

pathway_count = 100
ignition_count = 50
perturb_percent = 0.5 #this is the percent increase or decrease that will be applied to each 
#                       perturbed parameter in the perturbed polcies

### STEP 1 ######################################################
#   Generate a set of pathways (100s) using a coin-toss policy

print("Creating original pathways with coin-toss policy")
FGPO.createFireGirlPathways(pathway_count,ignition_count)


### STEP 2 ######################################################
#   Calculate the optimal policy using my surrogate obj fn (though if I could, both would be far better)

print("Beginning Policy Optimzation")
FGPO.USE_AVE_PROB = True
results = FGPO.optimizePolicy()
print("Policy Optimization Complete: Parameters are:")
print(str(FGPO.Policy.b))

### STEP 3 ######################################################
#   Create a large set of perturbations of that optimal policy

#copy the values of the optimal policy
pol_optim = []
for i in range(11):
    pol_optim.append(FGPO.Policy.b[i] + 1.0 - 1.0)

pert_pols = []
for i in range(11):
    #make new copies of the optimal policy
    pol_copy1 = []
    pol_copy2 = []
    for j in range(11):
        pol_copy1.append(pol_optim[j] + 1.0 - 1.0)
        pol_copy2.append(pol_optim[j] + 1.0 - 1.0)
    
    #perturb the copied policies at index i
    pol_copy1[i] *= (1 + perturb_percent)  # increase by this percent
    pol_copy2[i] *= (1 - perturb_percent)  # decrease by this percent
    
    #add the perturbed copies to the list
    pert_pols.append(pol_copy1)
    pert_pols.append(pol_copy2)
    
#print(str(pert_pols))