from FireGirlPathway import *
from numpy import mean, std
from scipy.stats import t  #t distribution and stats


"""This modules holds many functions that define basic stats on FireGirl pathways

Note: Most functions of this class accept a list of FireGirlPathway objects on which
to run the statistic(s) in question.
"""


def suppression_cost_stats_by_year(pathway_set):
    """From a list of FireGirlPathway objects, return summary statistics of suppression costs by year

    Args
    pathway_set: a list of at least one FireGirlPathway object

    Returns
    A list with four elements:
    -Element 0: A list containing the yearly average suppression costs over all pathways in the set. The first 
    element of the list will be the average suppresion cost for the first year of EACH pathway, and so on.

    -Element 1: A list containing the maximum suppresion cost of any pathway during that year.

    -Element 2: A list containing the minimum suppresion cost of any pathway during that year.

    -Element 3: A list containing the standard error of the yearly averages in Element 0

    -Element 4: A list containing the upper bound of the 95% confidence interval

    -Element 5: A list containing the lower bound of the 95% confidence interval
    """

    #checking for an empty input list
    if len(pathway_set) < 1:
        #it's empty, so return an equally empty result string
        return [[],[],[]]

    #Get averages and standard errors for each year
    yearly_ave = []
    yearly_stdev = []
    yearly_max = []
    yearly_min = []
    yearly_confidence_upper = []
    yearly_confidence_lower = []

    #how many years are there in these pathways?
    # assuming they all have the same number of events, query the first pathway in the list, and get the lenght
    # of it's ignition_events list
    years = len(pathway_set[0].ignition_events)

    #for each year, look in each pathway and add it's suppression cost to a list
    for y in range(years):
        this_years_sup_cost = []

        for pw in pathway_set:
            #add this pathway's suppression cost for this year to the list
            this_years_sup_cost.append( pw.yearly_suppression_costs[y] )

        #finished with all pathways at this year, so the list holds all year=y suppression costs

        #add a new element to the _ave and _stdev lists and add this year's stat to each
        yearly_ave.append( mean(this_years_sup_cost) )
        yearly_stdev.append( std(this_years_sup_cost) )
        yearly_min.append( min(this_years_sup_cost) )
        yearly_max.append( max(this_years_sup_cost) )

        #get the t-stat for a 95% confidence interval for sample of this size
        #this returns a list with the [lower , upper] stats, which are equal and opposite if centered 
        # around the mean, as ours are.
        tstat = t.interval(0.95, len(this_years_sup_cost) )

        #the upper and lower confidence intervals are calculated as
        #  Upper = Mean + (tstat) * (standard error of the mean)
        #  Lower = Mean - (tstat) * (standard error of the mean)

        upper_conf = yearly_ave[y] + (  tstat[0] * yearly_stdev[y]  )
        lower_conf = yearly_ave[y] - (  tstat[0] * yearly_stdev[y]  )

        #add them to the list
        yearly_confidence_upper.append(upper_conf) 
        yearly_confidence_lower.append(lower_conf) 

    #finished with ALL years

    #return a list with each list of stats
    return [yearly_ave, yearly_max, yearly_min, yearly_stdev, yearly_confidence_upper, yearly_confidence_lower]

def timber_harvest_stats_by_year(pathway_set):
    """From a list of FireGirlPathway objects, return summary statistics of harvest values by year

    Args
    pathway_set: a list of at least one FireGirlPathway object

    Returns
    A list with four elements:
    -Element 0: A list containing the yearly average harvest values over all pathways in the set. The first 
    element of the list will be the average harvest values for the first year of EACH pathway, and so on.

    -Element 1: A list containing the maximum harvest values of any pathway during that year.

    -Element 2: A list containing the minimum harvest values of any pathway during that year.

    -Element 3: A list containing the standard error of the yearly averages in Element 0

    -Element 4: A list containing the upper bound of the 95% confidence interval

    -Element 5: A list containing the lower bound of the 95% confidence interval
    """

    #checking for an empty input list
    if len(pathway_set) < 1:
        #it's empty, so return an equally empty result string
        return [[],[],[]]

    #Get averages and standard errors for each year
    yearly_ave = []
    yearly_stdev = []
    yearly_max = []
    yearly_min = []
    yearly_confidence_upper = []
    yearly_confidence_lower = []

    #how many years are there in these pathways?
    # assuming they all have the same number of events, query the first pathway in the list, and get the lenght
    # of it's ignition_events list
    years = len(pathway_set[0].ignition_events)

    #for each year, look in each pathway and add it's harvest value to a list
    for y in range(years):
        this_years_harvest = []

        for pw in pathway_set:
            #add this pathway's harvest value for this year to the list
            this_years_harvest.append( pw.yearly_logging_totals[y] )

        #finished with all pathways at this year, so the list holds all year=y harvest value

        #add a new element to the _ave and _stdev lists and add this year's stat to each
        yearly_ave.append( mean(this_years_harvest) )
        yearly_stdev.append( std(this_years_harvest) )
        yearly_min.append( min(this_years_harvest) )
        yearly_max.append( max(this_years_harvest) )

        #get the t-stat for a 95% confidence interval for sample of this size
        #this returns a list with the [lower , upper] stats, which are equal and opposite if centered 
        # around the mean, as ours are.
        tstat = t.interval(0.95, len(this_years_harvest) )

        #the upper and lower confidence intervals are calculated as
        #  Upper = Mean + (tstat) * (standard error of the mean)
        #  Lower = Mean - (tstat) * (standard error of the mean)

        upper_conf = yearly_ave[y] + (  tstat[0] * yearly_stdev[y]  )
        lower_conf = yearly_ave[y] - (  tstat[0] * yearly_stdev[y]  )

        #add them to the list
        yearly_confidence_upper.append(upper_conf) 
        yearly_confidence_lower.append(lower_conf) 

    #finished with ALL years

    #return a list with each list of stats
    return [yearly_ave, yearly_max, yearly_min, yearly_stdev, yearly_confidence_upper, yearly_confidence_lower]

def growth_stats_by_year(pathway_set):
    """From a list of FireGirlPathway objects, return summary statistics of timber growth by year

    Args
    pathway_set: a list of at least one FireGirlPathway object

    Returns
    A list with four elements:
    -Element 0: A list containing the yearly average growth over all pathways in the set. The first 
    element of the list will be the average growth for the first year of EACH pathway, and so on.

    -Element 1: A list containing the maximum growth of any pathway during that year.

    -Element 2: A list containing the minimum growth of any pathway during that year.

    -Element 3: A list containing the standard error of the yearly averages in Element 0

    -Element 4: A list containing the upper bound of the 95% confidence interval

    -Element 5: A list containing the lower bound of the 95% confidence interval
    """

    #checking for an empty input list
    if len(pathway_set) < 1:
        #it's empty, so return an equally empty result string
        return [[],[],[]]

    #Get averages and standard errors for each year
    yearly_ave = []
    yearly_stdev = []
    yearly_max = []
    yearly_min = []
    yearly_confidence_upper = []
    yearly_confidence_lower = []

    #how many years are there in these pathways?
    # assuming they all have the same number of events, query the first pathway in the list, and get the lenght
    # of it's ignition_events list
    years = len(pathway_set[0].ignition_events)

    #for each year, look in each pathway and add it's harvest value to a list
    for y in range(years):
        this_years_growth = []

        for pw in pathway_set:
            #add this pathway's growth for this year to the list
            this_years_growth.append( pw.yearly_growth_totals[y] )

        #finished with all pathways at this year, so the list holds all year=y growth

        #add a new element to the _ave and _stdev lists and add this year's stat to each
        yearly_ave.append( mean(this_years_growth) )
        yearly_stdev.append( std(this_years_growth) )
        yearly_min.append( min(this_years_growth) )
        yearly_max.append( max(this_years_growth) )

        #get the t-stat for a 95% confidence interval for sample of this size
        #this returns a list with the [lower , upper] stats, which are equal and opposite if centered 
        # around the mean, as ours are.
        tstat = t.interval(0.95, len(this_years_growth) )

        #the upper and lower confidence intervals are calculated as
        #  Upper = Mean + (tstat) * (standard error of the mean)
        #  Lower = Mean - (tstat) * (standard error of the mean)

        upper_conf = yearly_ave[y] + (  tstat[0] * yearly_stdev[y]  )
        lower_conf = yearly_ave[y] - (  tstat[0] * yearly_stdev[y]  )

        #add them to the list
        yearly_confidence_upper.append(upper_conf) 
        yearly_confidence_lower.append(lower_conf) 

    #finished with ALL years

    #return a list with each list of stats
    return [yearly_ave, yearly_max, yearly_min, yearly_stdev, yearly_confidence_upper, yearly_confidence_lower]

def fire_stats_by_year(pathway_set):
    """From a list of FireGirlPathway objects, return descriptive statistics of fires, by yearly_logging_totals

    Arguements
    pathway_set: A list of FireGirlPathway objects

    Returns a list with the following elements:
    -Element 0: A list containing various cells-burned stats
    ---Element 0: A list by year containing average number of cells burned in this years fires accross pathways
    ---Element 1: A list by year containing the smallest number of cells burned for any fire in a given year
    ---Element 2: A list by year containing the largest number of cells burned for any fire in a given year
    ---Element 3: A list, by year, containing standard deviations of cells burned for each year
    ---Element 4: A list, by year, containing upper confidence intervals on cells burned
    ---Element 5: A list, by year, containing lower confidence intervals on cells burned

    -Element 1: A list containing various timber-lost stats
    ---Element 0: A list, by year, containing the average timber lost to fire each year
    ---Element 1: A list, by year, containing the smallest timber lost to a fire in any pathway in a given year
    ---Element 2: A list, by year, containing the largest timber lost to a fire in any pathway in a given year
    ---Element 3: A list, by year, containing standard deviations of timber lost for each year
    ---Element 4: A list, by year, containing upper confidence intervals on timber lost
    ---Element 5: A list, by year, containing lower confidence intervals on timber lost

    -Element 2: A list, by year, of the number of pathways which suppressed their fires this year
    """

    #checking for an empty input list
    if len(pathway_set) < 1:
        #it's empty, so return an equally empty result string
        return [[],[],[],[],[],[],[],[],[],[]]

    #things to compile
    cells_burned_ave = []
    cells_burned_max = []
    cells_burned_min = []
    cells_burned_std = []
    cells_burned_confidence_upper = []
    cells_burned_confidence_lower = []
    timber_lost_ave = []
    timber_lost_max = []
    timber_lost_min = []
    timber_lost_std = []
    timber_lost_confidence_upper = []
    timber_lost_confidence_lower = []
    suppress_decisions = []

    #how many years are there in these pathways?
    # assuming they all have the same number of events, query the first pathway in the list, and get the lenght
    # of it's ignition_events list
    years = len(pathway_set[0].ignition_events)

    #get a new value for each of the above lists, for each year
    for y in range(years):
        this_years_cells_burned = []
        this_years_timber_lost = []
        this_years_suppress_decisions = 0

        #look through each pathway and add their value for year=y to cells_burned, timber_lost, and supp_decisions
        for pw in pathway_set:
            #in a pathway's ignition_events list, the ignition records each have an "outcomes" member
            #an ignition_record.getOutcomes() call returns a list in the following format:
            #  [timber_loss, cells_burned, sup_cost, end_time]
            outcomes = pw.ignition_events[y].getOutcomes()
            this_years_timber_lost.append( outcomes[0] )
            this_years_cells_burned.append( outcomes[1] )
            
            #likewise, calling an iginiton event object's .getChoice() method will return a True if the simulator
            #  suppressed that fire, and a False if it did not.
            if pw.ignition_events[y].getChoice():
                this_years_suppress_decisions += 1

        #we've got all the cells_burned, timber_lost, and suppress decisions for each pathway for this year
        cells_burned_ave.append( mean(this_years_cells_burned) )
        cells_burned_max.append(  max(this_years_cells_burned) )
        cells_burned_min.append(  min(this_years_cells_burned) )
        cells_burned_std.append(  std(this_years_cells_burned) )
        timber_lost_ave.append(  mean(this_years_timber_lost) )
        timber_lost_max.append(   max(this_years_timber_lost) )
        timber_lost_min.append(   min(this_years_timber_lost) )
        timber_lost_std.append(   std(this_years_timber_lost) )

        suppress_decisions.append( this_years_suppress_decisions )

        #get the t-stat for a 95% confidence interval for sample of this size
        #this returns a list with the [lower , upper] stats, which are equal and opposite if centered 
        # around the mean, as ours are.
        tstat = t.interval(0.95, len(this_years_cells_burned) )

        #the upper and lower confidence intervals are calculated as
        #  Upper = Mean + (tstat) * (standard error of the mean)
        #  Lower = Mean - (tstat) * (standard error of the mean)

        cells_burned_upper_conf = cells_burned_ave[y] + (  tstat[0] * cells_burned_std[y]  )
        cells_burned_lower_conf = cells_burned_ave[y] - (  tstat[0] * cells_burned_std[y]  )
        timber_lost_upper_conf = timber_lost_ave[y] + (  tstat[0] * timber_lost_std[y]  )
        timber_lost_lower_conf = timber_lost_ave[y] - (  tstat[0] * timber_lost_std[y]  )

        cells_burned_confidence_upper.append( cells_burned_upper_conf )
        cells_burned_confidence_lower.append( cells_burned_lower_conf )
        timber_lost_confidence_upper.append( timber_lost_upper_conf )
        timber_lost_confidence_lower.append( timber_lost_lower_conf )

    #All Years are finished, so compile the return lists

    cells_burned_stats = [cells_burned_ave, cells_burned_min, cells_burned_max, cells_burned_std, cells_burned_confidence_upper, timber_lost_confidence_lower]
    timber_lost_stats = [timber_lost_ave, timber_lost_min, cells_burned_max, timber_lost_std, timber_lost_confidence_upper, timber_lost_confidence_lower]

    return [cells_burned_stats, timber_lost_stats, suppress_decisions]



