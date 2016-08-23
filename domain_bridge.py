from FireGirlOptimizer import *
from FireGirlStats import *
import os.path
import time

def initialize():
    """
    Return the initialization object for the FireGirl domain.
    """
    mdpvis_initialization_object = {

        # The settings to apply at initialization time
        "mdpvis_settings": {
            "domain_instructions": "todo",
            "domain_cover_image": "todo",
            "saved states": [
                {
                    "description": "A set of interesting queries",
                    "href": "todo"
                }
            ]
        },

        # The control panels that appear at the top of the screen
        "parameter_collections": [
            {
                "panel_title": "Reward",
                "panel_icon": "glyphicon-king",
                "panel_description": "Define the parameters of the optimization algorithm.",
                "default_rendering": "parallel",
                "quantitative": [  # Real valued parameters
                                   {
                                       "name": "Discount",
                                       "description": "The per-year discount",
                                       "current_value": 1,
                                       "max": 1,
                                       "min": 0,
                                       "step": 1,
                                       "units": "Unitless"
                                   },
                                   {
                                      "name": "Suppression Fixed Cost",
                                      "description": "cost per day of suppression",
                                      "current_value": 500,
                                      "max": 999999,
                                      "min": 0,
                                      "step": 10,
                                      "units": "$"
                                   },
                                   {
                                      "name": "Suppression Variable Cost",
                                      "description": "cost per hectare of suppression",
                                      "current_value": 500,
                                      "max": 999999,
                                      "min": 0,
                                      "step": 10,
                                      "units": "$"
                                  }
                ]
            },
            {
                "panel_title": "Policy",
                "panel_icon": "glyphicon-random",
                "panel_description": "Define the parameters of the policies used to generate trajectories.",
                "default_rendering": "parallel", # Default to a parallel plot.
                "quantitative": [  # Real valued parameters
                           {"name": "Constant",
                             "description":"for the intercept",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name": "Date",
                             "description":"for each day of the year",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name": "Days Left",
                             "description":"for each day left in the year",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name":"Temperature",
                             "description":"for air temperature at the time of an ignition",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name": "Wind Speed",
                             "description":"for wind speed at the time of an ignition",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name": "Timber Value",
                             "description":"for the timber value at an ignition location",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name": "Timber Value 8",
                             "description":"for the average timber value in the 8 neighboring stands",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name": "Timber Value 24",
                             "description":"for the average timber value in the 24 neighboring stands",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name": "Fuel Load",
                             "description":"for the fuel load at an ignition location",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                              "step": 1},
                            {"name": "Fuel Load 8",
                             "description":"for the average fuel load in the 8 neighboring stands",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1},
                            {"name": "Fuel Load 24",
                             "description":"for the average fuel load in the 24 neighboring stands",
                             "current_value": 0, "max": 10, "min":-10, "units": "",
                             "step": 1}
                ]
            },
            {
                "panel_title": "Transition Function",
                "panel_icon": "glyphicon-retweet",
                "panel_description": "Define the MDP transition function and sampling effort.",
                "default_rendering": "parallel", # Default to a radar plot. User can switch to input elements.
                "quantitative": [  # Real valued parameters
                                    {"name": "Harvest Percent",
                                     "description": "timber harvest rate as a percent of annual increment",
                                     "current_value": 0.95, "max": 1, "min": 0, "units": "%", "step": 1},
                                    {"name": "Minimum Timber Value",
                                     "description":"the minimum timber value required before harvest is allowed",
                                     "current_value": 50, "max":9999, "min": 0, "units": "$", "step": 1},
                                    {"name": "Slash Remaning",
                                     "description": "the amount of fuel load (slash) left after a harvest",
                                     "current_value": 10, "max":9999, "min": 0, "units": "#", "step": 1},
                                    {"name": "Fuel Accumulation",
                                     "description": "the amount of fuel load that accumulates each year",
                                     "current_value": 2, "max":9999, "min": 0, "units": "#", "step": 1},
                                    {"name": "Suppression Effect",
                                     "description": "the reduction in fire spread rate as the result of suppression",
                                     "current_value": 0.5, "max":1, "min": 0, "units": "%", "step": 1},
                                     {"name": "Use Original Bugs",
                                      "description": "set to 0 to use original bugs. 1 (or non-zero) to use the patches.",
                                      "current_value": 0, "max":1, "min": 0, "units": "~", "step": 1},
                                     {"name": "Growth Model",
                                      "description": "set to 1 to use original model; or 2 for updated model.",
                                      "current_value": 1, "max":2, "min": 1, "units": "~", "step": 1}
                ]
            },
            {
                "panel_title": "Sampling Effort",
                "panel_icon": "glyphicon-th-list",
                "panel_description": "Define how much you want to sample.",
                "default_rendering": "parallel", # Default to a parallel plot. User can switch to input elements.
                "quantitative": [  # Real valued parameters
                                    {"name": "Years to simulate",
                                     "description": "how far to look into the future",
                                     "current_value": 10, "max": 150, "min": 0, "units": "Y", "step": 1},
                                    {"name": "Futures to simulate",
                                     "description": "how many stochastic futures to generate",
                                     "current_value": 25, "max": 1000, "min": 0, "units": "#", "step": 1},
                                    {"name": "Landscape Size",
                                     "description": "how many cells wide and tall should the landscape be. Min:9, Max:129",
                                     "current_value": 21, "max": 129, "min": 9, "units": "#", "step": 1}
                ]
            }
        ]
    }
    return mdpvis_initialization_object

def optimize(query):
    """
    Return a newly optimized query.
    """
    pathway_count = query["Futures to simulate"]
    years = query["Years to simulate"]


    #creating optimization objects
    opt = FireGirlPolicyOptimizer()

    #giving the simulation parameters to opt, so that it can pass
    # them on to it's pathways as it creates them
    mungedQuery = {}
    for k in query.keys():
        mungedQuery[k] = float(query[k])
    opt.setFireGirlModelParameters(mungedQuery)

    #setting policy as well
    pol = FireGirlPolicy()
    pol.setParams([float(i) for i in [query["Constant"],
                   query["Date"],
                   query["Days Left"],
                   query["Temperature"],
                   query["Wind Speed"],
                   query["Timber Value"],
                   query["Timber Value 8"],
                   query["Timber Value 24"],
                   query["Fuel Load"],
                   query["Fuel Load 8"],
                   query["Fuel Load 24"],
                  ]])

    #assigning the policy to opt, so that it can use it in simulations.
    opt.setPolicy(pol)


    #creating pathways
    opt.createFireGirlPathways(int(pathway_count),int(years))

    #set desired objective function
    if "Objective Function" in query.keys():
        opt.setObjFn(query["Objective Function"])

    #doing one round of optimization
    opt.optimizePolicy()

    #pulling the policy variables back out
    learned_params = opt.Policy.getParams()

    #TODO make this robust to FireWoman policies
    dict_new_pol = {}
    dict_new_pol["Constant"] = learned_params[0]
    dict_new_pol["Date"] = learned_params[1]
    dict_new_pol["Days Left"] = learned_params[2]
    dict_new_pol["Temperature"] = learned_params[3]
    dict_new_pol["Wind Speed"] = learned_params[4]
    dict_new_pol["Timber Value"] = learned_params[5]
    dict_new_pol["Timber Value 8"] = learned_params[6]
    dict_new_pol["Timber Value 24"] = learned_params[7]
    dict_new_pol["Fuel Load"] = learned_params[8]
    dict_new_pol["Fuel Load 8"] = learned_params[9]
    dict_new_pol["Fuel Load 24"] = learned_params[10]

    return dict_new_pol

def rollouts(query):
    """
    Return a set of rollouts for the given parameters.
    """

    pathway_count = int(query["Futures to simulate"])
    years = int(query["Years to simulate"])
    start_ID = 0

    #generate 100 rollouts
    opt = FireGirlPolicyOptimizer()
    opt.setObjFn("J1")
    #opt.setObjFn("J2")
    opt.SILENT = True

    mungedQuery = {}
    for k in query.keys():
        mungedQuery[k] = float(query[k])

    #setting policy...
    #This is brittle, and will not work directly with FireWoman data... or with future versions
    # of FireGirl if new features get added...
    pol = FireGirlPolicy()
    pol.setParams([mungedQuery["Constant"],
                   mungedQuery["Date"],
                   mungedQuery["Days Left"],
                   mungedQuery["Temperature"],
                   mungedQuery["Wind Speed"],
                   mungedQuery["Timber Value"],
                   mungedQuery["Timber Value 8"],
                   mungedQuery["Timber Value 24"],
                   mungedQuery["Fuel Load"],
                   mungedQuery["Fuel Load 8"],
                   mungedQuery["Fuel Load 24"],
                  ])

    #setting the policy in the optimizer, which will pass it to each created pathway
    opt.setPolicy(pol)

    #giving the optimizer custom model parameters
    opt.setFireGirlModelParameters(mungedQuery)

    event_number = -1
    pathway_number = -1
    layer = -1
    def file_name(max_steps=years, event_number=event_number, pathway_number=pathway_number, layer=layer, constant=mungedQuery["Constant"], date=mungedQuery["Date"],\
        days=mungedQuery["Days Left"], temp=mungedQuery["Temperature"], wind=mungedQuery["Wind Speed"],\
        timberv=mungedQuery["Timber Value"], timberv8=mungedQuery["Timber Value 8"], timberv24=mungedQuery["Timber Value 24"], fuel=mungedQuery["Fuel Load"],\
        fuel8=mungedQuery["Fuel Load 8"], fuel24=mungedQuery["Fuel Load 24"],
        Discount=mungedQuery["Discount"],
        SuppressionFixedCost=mungedQuery["Suppression Fixed Cost"],
        SuppressionVariableCost=mungedQuery["Suppression Variable Cost"],
        HarvestPercent=mungedQuery["Harvest Percent"],
        MinimumTimberValue=mungedQuery["Minimum Timber Value"],
        SlashRemaning=mungedQuery["Slash Remaning"],
        FuelAccumulation=mungedQuery["Fuel Accumulation"],
        SuppressionEffect=mungedQuery["Suppression Effect"]
        ):
        return "static/a-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-.png".format(
            max_steps, event_number, pathway_number, layer, constant, date,\
            days, temp, wind, timberv, timberv8, timberv24, fuel, fuel8, fuel24,
            Discount,
            SuppressionFixedCost,
            SuppressionVariableCost,
            HarvestPercent,
            MinimumTimberValue,
            SlashRemaning,
            FuelAccumulation,
            SuppressionEffect
            )

    #creating landscapes. The function will enforce the custom model parameters
    opt.createFireGirlPathways(pathway_count,years,start_ID)

    #outermost list to collect one sub-list for each pathway, etc...
    return_list = []

    #parse the data needed...
    for pw in opt.pathway_set:
        #new ignition events list for this pathway
        year_values = []
        for ign in pw.ignition_events:

            #get the dictionary representation of the ignition
            features = ign.getDictionary()

            #fill the total's dictionary
            features["Harvest Value"] = pw.getHarvest(ign.year)
            #features["Suppression Cost"] = pw.getSuppressionCost(ign.year) #already reported in ign.getDictionary()
            features["Growth"] = pw.getGrowth(ign.year)

            features["image row"] = [file_name(layer="timber", event_number=ign.year, pathway_number=pw.ID_number),
                                     file_name(layer="fuel", event_number=ign.year, pathway_number=pw.ID_number),
                                     file_name(layer="composite", event_number=ign.year, pathway_number=pw.ID_number),
                                     file_name(layer="timber10", event_number=ign.year, pathway_number=pw.ID_number)]

            #TODO - Fix for Discount Rate
            features["Discounted Reward"] = features["Harvest Value"] - features["Suppression Cost"]

            features["Event Number"] = ign.year

            #NOTE:  This will be the same number for all ignitions in this pathway. It's the
            # id number that a pathway uses to instantiate its random seed 
            features["Pathway Number"] = pw.ID_number

            #adding cumulative measurements, from the start, up to this year
            features["Cumulative Harvest Value"] = pw.getHarvestFrom(0, ign.year)
            features["Cumulative Growth"] = pw.getGrowthFrom(0, ign.year)
            features["Cumulative Timber Loss"] = pw.getTimberLossFrom(0, ign.year)
            features["Cumulative Suppression Cost"] = pw.getSuppressionFrom(0, ign.year)
            if features["Suppression Choice"]:
                features["Suppression Choice"] = 1
            else:
                features["Suppression Choice"] = 0

            #add this ignition event + year details to this pathway's list of dictionaries
            year_values.append(features)

        #the events list for this pathway has been filled, so add it to the return list
        return_list.append(year_values)

    #done with all pathways

    return return_list

# Used to ensure the images are not generated for every image requested in a trajectory
generatingImages = False

def generate_state_images(image_file_name):
    """
    Save the state images to the static folder if they have been requested, then start returning images
    """
    global generatingImages # hack
    if generatingImages:
        print "sleeping"
        time.sleep(2)
        return generate_state_images(image_file_name)

    if os.path.isfile(image_file_name):
        return
    else:
        generatingImages = True

    _, max_steps, event_number, pathway_number, layer, constant, date,\
    days, temp, wind, timberv, timberv8, timberv24, fuel,\
    fuel8, fuel24,\
    Discount,\
    SuppressionFixedCost,\
    SuppressionVariableCost,\
    HarvestPercent,\
    MinimumTimberValue,\
    SlashRemaning,\
    FuelAccumulation,\
    SuppressionEffect, _ = image_file_name.split("-")

    max_steps = int(max_steps)
    event_number = int(event_number)
    pathway_number = int(pathway_number)

    #creating optimization objects
    opt = FireGirlPolicyOptimizer()

    #giving the simulation parameters to opt, so that it can pass
    # them on to it's pathways as it creates them
    opt.setFireGirlModelParameters(
      {
        "Discount": float(Discount),
        "Suppression Fixed Cost": float(SuppressionFixedCost), 
        "Suppression Variable Cost": float(SuppressionVariableCost),
        "Harvest Percent": float(HarvestPercent),
        "Minimum Timber Value": float(MinimumTimberValue),
        "Slash Remaning": float(SlashRemaning),
        "Fuel Accumulation": float(FuelAccumulation),
        "Suppression Effect": float(SuppressionEffect)
      }
    )

    #setting policy as well
    pol = FireGirlPolicy()
    pol.setParams([float(i) for i in [constant,
                   date,
                   days,
                   temp,
                   wind,
                   timberv,
                   timberv8,
                   timberv24,
                   fuel,
                   fuel8,
                   fuel24
                  ]])

    #assigning the policy to opt, so that it can use it in simulations.
    opt.setPolicy(pol)

    #Setting opt to tell it's pathway(s) to remember their histories
    #un-needed, since we're just re-creating the pathway of interest anyway
    #opt.PATHWAYS_RECORD_HISTORIES = True 

    opt.SILENT = True

    #creating pathway with no years... this will generate the underlying landscape and set
    #  all the model parameters that were assigned earlier.
    opt.createFireGirlPathways(1, 0, pathway_number)

    #now incrementing the years
    #because we start with the final year, and then skip backward showing every few landscapes,
    #we may have to skip over several of the first landscapes before we start showing any
    start = event_number

    #manually telling the pathway to do the first set of years
    opt.pathway_set[0].doYears(start)

    def file_name(event_number=event_number, pathway_number=pathway_number, layer=layer, constant=constant, date=date,\
        days=days, temp=temp, wind=wind, timberv=timberv, timberv8=timberv8, timberv24=timberv24, fuel=fuel,\
        fuel8=fuel8, fuel24=fuel24,
        Discount=Discount,
        SuppressionFixedCost=SuppressionFixedCost,
        SuppressionVariableCost=SuppressionVariableCost,
        HarvestPercent=HarvestPercent,
        MinimumTimberValue=MinimumTimberValue,
        SlashRemaning=SlashRemaning,
        FuelAccumulation=FuelAccumulation,
        SuppressionEffect=SuppressionEffect):
        return "static/a-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-.png".format(
            max_steps, event_number, pathway_number, layer, constant, date,\
            days, temp, wind, timberv, timberv8, timberv24, fuel, fuel8, fuel24,
            Discount,
            SuppressionFixedCost,
            SuppressionVariableCost,
            HarvestPercent,
            MinimumTimberValue,
            SlashRemaning,
            FuelAccumulation,
            SuppressionEffect
            )

    #and save it's images
    opt.pathway_set[0].saveImage(file_name(layer="timber", event_number=0, pathway_number=pathway_number), "timber")
    opt.pathway_set[0].saveImage(file_name(layer="fuel", event_number=0, pathway_number=pathway_number), "fuel")
    opt.pathway_set[0].saveImage(file_name(layer="composite", event_number=0, pathway_number=pathway_number), "composite")
    opt.pathway_set[0].saveImage(file_name(layer="timber10", event_number=0, pathway_number=pathway_number), "timber", 10)

    #now loop through the rest of the states
    for i in range(0, max_steps+1):
        #do the next set of years
        opt.pathway_set[0].doYears(1)

        #save the images
        opt.pathway_set[0].saveImage(file_name(layer="timber", event_number=i, pathway_number=pathway_number), "timber")
        opt.pathway_set[0].saveImage(file_name(layer="fuel", event_number=i, pathway_number=pathway_number), "fuel")
        opt.pathway_set[0].saveImage(file_name(layer="composite", event_number=i, pathway_number=pathway_number), "composite")
        opt.pathway_set[0].saveImage(file_name(layer="timber10", event_number=i, pathway_number=pathway_number), "timber", 10)

    generatingImages = False # Completed generation
    

def state(query):
    """
    Return a series of images up to the requested event number.
    """
    
    # get the image identifier information
    
    image_file_name = query["image"]
    print "generating %s" % image_file_name
    generate_state_images(image_file_name)
    return image_file_name
