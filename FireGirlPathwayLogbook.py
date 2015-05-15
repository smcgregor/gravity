class FireGirlIgnitionRecord:
    #This class holds the salient information from any igition, either in FireGirl or
    #  in FireWoman pathways.

    #self.features is a list of feature values known at the beginning of each ignition
    #   event. This should only contain information that a fire manager would know at 
    #   the time of ignition, and on which they could base their suppression decisions.

    #self.policy_prob holds the probability of suppresion given by a FireGirlPolicy object.

    #self.policy_choice is a boolean flag which records True if the fire was suppressed and
    #   False if the fire was not suppressed.

    #self.outcomes is a list of any information about the results of the fire, mostly intended
    #   for post hoc analysis of the program.

    #self.feature_labels is an optional list of strings describing what each value in 
    #   self.features means.

    #self.outcome_labels is an optional list of strings describing what each value in 
    #   self.outcomes means.

    def __init__(self):
        self.features = []
        self.features_raw = []  #this is a storage array for the orginal feature values when
        #                         an outside function does a normalization routine
        self.policy_prob = 1
        self.policy_choice = False
        self.outcomes = []
        self.feature_labels = []
        self.outcome_labels = []
        self.year = 0
        self.burn_time = 0
        self.location = []

    def getYear(self):
        return self.year

    def getProb(self):
        return self.policy_prob

    def getChoice(self):
        return self.policy_choice

    def getFeatures(self):
        return self.features

    def getOutcomes(self):
        return self.outcomes

    def getFeatureLabels(self):
        return self.feature_labels

    def getOutcomeLabels(self):
        return self.outcome_labels

    def getBurnTime(self):
        return self.burn_time

    def setYear(self, year):
        self.year = year

    def setChoice(self, choice):
        self.policy_choice = choice

    def setProb(self, prob):
        self.policy_prob = prob

    def setFeatures(self, feature_list):
        self.features = feature_list

    def setOutcomes(self, outcome_list):
        self.outcomes = outcome_list

    def setFeatureLabels(self, labels):
        self.feature_labels = labels

    def setOutcomeLabels(self, labels):
        self.outcome_labels = labels

    def setBurnTime(self, time):
        self.burn_time = time

    def calcNewProb(self, policy_object):
        #this function will use the record's CURRENT set of features and ask the
        #  policy it is given as an arguement what the new suppression probability will be.
        #  It does NOT assign that probability, at the moment.

        prob = policy_object.calcProb(self.features)

        return prob

    def getDictionary(self):
        """Returns dictionary representation of this ignition's primary features

        """
        d = {}

        #check if the features have been normalized by checking the length of the
        # _raw list. It only gets filled during the normalization process
        if len(self.features_raw) > 0:
            #normalization has happened, so use the raw values
            for f in range(len(self.features_raw)):
                d[self.feature_labels[f]] = self.features_raw[f]

        else:
            #normalization hasn't happened, so just use the orginal features
            for f in range(len(self.features)):
                d[self.feature_labels[f]] = self.features[f]


        d["Policy Probability"] = self.policy_prob
        d["Suppression Choice"] = self.policy_choice

        #add outcomes
        for o in range(len(self.outcomes)):
            #adding keys/pairs from outcomes, which is set to
            # "Timber Loss", "Cells Burned", "Suppression Cost", "Burn Time" in FGPathway...
            d[self.outcome_labels[o]] = self.outcomes[o]

        d["Year"] = self.year
        #d["Burn Time"] = self.burn_time #this one is already repored in self.outcomes
        d["Location X"] = self.location[0]
        d["Location Y"] = self.location[1]

        return d

        
class FireGirlFireLog:
    #This class defines a logbook for a single fire. The location of each cell
    #that burns, and the local fire time (not the pathway year) is recorded.
        
    def __init__(self, year):

        #a list to hold individual burn events <- meaning a single cell igniting
        self.burn_events = []
        
        #a record of the year in which this fire takes place
        self.year = year
        
        #records of overall fire results
        self.cells_burned = 0
        self.cells_crowned = 0
        self.timber_loss = 0

        #burn maps (booleans)
        self.map_burned = []
        self.map_crowned = []
    
    
    def addIgnitionEvent(self, time, location, spread_rate, crown_burned):
        #this function takes the time and location of an ignition and other 
        #  pertinent information and adds it to the list.
        
        this_event = [time, location, spread_rate, crown_burned, "ignition"]
        self.burn_events.append(this_event)
    
    def updateResults(self, timber_loss, cells_burned, cells_crowned):
        self.cells_burned = cells_burned
        self.cells_crowned = cells_crowned
        self.timber_loss = timber_loss
        
    def printBasicInfo(self):
        print("Year " + str(self.year) + " Fire:  Cells burned = " + str(self.cells_burned) + "   Timber Loss = " + str(self.timber_loss) )
    
    def printFireHistory(self):
        for i in range(len(self.burn_events)):
            b = self.burn_events[i]
            print("Ignition at time " + str( round(b[0],3) )     ),
            print("   Loc : " + str(b[1]) ),
            print("   SprdRt: " + str(  round(b[2],3)   )),
            print("   CrownBurn: " + str(b[3]))


