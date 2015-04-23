import math

class FireGirlPolicy:
    #This is a the base class for both the FireGirl_Policy and FireWoman_Policy classes
    #Note: It is intended that this class will not be used on it's own, but rather only
    #  in it's inherited forms.

    #If a list of parameters is passed in, the local b values will be set accordingly,
    #  and SETALL and COUNT will be ignored.

    #If SETALL is set and params==None, then all parameters will be set to the given value

    #COUNT is the total number of parameters to set, so assuming SETALL is used (no param list)
    #  then the SETALL value will be assigned this many times
    
    def __init__(self, params=None, SETALL=None, COUNT=None):
        # a list of features, designed to be set repeatedly for each fire event
        self.features = []
        
        # a list of this policy's parameters.
        self.b = []

        #FLAGS for distinct, non-logistic policy types
        self.SUPPRESS_ALL = False
        self.LET_BURN = False

        
        #Checking for initialization values, and assigning them as appropriate
        if not params == None:
            self.b = params
        else:
            if not COUNT == None:
                if not SETALL == None:
                    for i in range(COUNT):
                        self.b.append(float(SETALL))
        
        #Because the logistic function can easily produce 0-values for very low probabilities, 
        #  we need to set a limit for what the lowest probability allowed is. Otherwise
        #  the product of any series of events is likely to be 0, because of even one very low probability
        self.probability_lower_limit = 0.001
        
        #likewise, since a choice that DOES NOT follow a rule when the probability is 1 will also produce 
        #  and effective probability of 0, there needs to be an upper limit as well.
        self.probability_upper_limit = 0.999

    def setSuppressAll(self):
        # this function flips the appropriate flags so that the policy will always return a 100% suppress decision
        self.SUPPRESS_ALL = True
        self.LET_BURN = False

    def setLetBurn(self):
        # this functions flips the appropriate flags so that the policy will always return a 0% suppress decision
        self.SUPPRESS_ALL = False
        self.LET_BURN = True

    def setUseParameters(self):
        # this function de-selects both the SUPPRESS_ALL and LET_BURN flags, so that the policy will return
        #  suppression decisions according to whatever it's parameters currently are.
        self.SUPPRESS_ALL = False
        self.LET_BURN = False

    def setParams(self, parameter_list):
        #this function takes a new list of parameters for the policy, and in doing so, also de-selects any
        #  previous let-burn or suppress-all behaviors that would otherwise ignore the new parameters
        self.SUPPRESS_ALL = False
        self.LET_BURN = False
        self.b = []
        for param in parameter_list:
            self.b.append(float(param) + 1.0 - 1.0) #+1 -1 is to strictly enforce a value being appended, rather than a reference

    def setFeatures(self, feature_list):
        self.features = []
        for feature in feature_list:
            self.features.append(float(feature) + 1.0 - 1.0)

    def getParams(self):
        return self.b

    def crossProduct(self, feature_list=None):
        #This function will return the crossproduct between each feature and it's 
        #  corresponding parameter beta value 

        #if no feature list is passed, just use what the Policy already has
        #otherwise, use what's been given.
        if not feature_list == None:
            self.features = feature_list
        
        cp = 0.0

        for i in range(len(self.features)):
            cp += self.features[i] * self.b[i]
            
        return cp

    def logistic(self, value):
        #This function calculates the simple logistic function value of the input
        try:
            return (  1.0 / (1.0 + math.exp(-value))  )
        except(OverflowError):
            #print("FireGirlPolicy.logistic() encountered and overflow error: returning 0")

            #an overflow error can only happen when value is very negative, resulting in too
            #  high a exp() value. In turn, this means the division goes to zero, as expected
            #  for a logistic function.
            return 0.0
    
    def calcProb(self, feature_list):
        #checking policy flags
        if self.SUPPRESS_ALL:
            return 1.0
        elif self.LET_BURN:
            return 0.0
        #None of the policy flags were set, so do the math and report a real policy decision
        else:
            self.features = feature_list
            cp = self.crossProduct()
            try:
                p = self.logistic(cp)
                
                #enforce lower limit on probabilities...
                if p < self.probability_lower_limit:
                    p = self.probability_lower_limit
                    
                #enforce upper limit on probabilities...
                if p > self.probability_upper_limit:
                    p = self.probability_upper_limit

                return p
            except(OverflowError):
                print("FGPolicy.calcProb() encountered and overflow error:")
                print("  crossproduct is: " + str(cp))
                return 0.0


 