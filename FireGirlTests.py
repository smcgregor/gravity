from FireGirlOptimizer import *
from FireGirlStats import *
from numpy import mean

class FireGirlTests:
    #This class is designed to house functions useful in testing and analyzing the behavior
    #  and data of FireGirl objects, including when they are interacting with FireWoman data

    def __init__(self):

        #FLAG: general directive for tests to give a one-three line summary of their results
        self.PRINT_SUMMARIES = True
        #FLAG: in addition to printing summary information, ALSO print all details
        self.PRINT_DETAILS = True
        #FLAG: REGARDLESS OF OTHER FLAGS, print no ouptuts
        self.SILENT = False

    def stats_test(self, pathway_count = 20, years=100, start_ID=0):
        """Short test of the FireGirlStats functions

        Note: At the moment, a coin-toss policy is being used...
        """

        if not self.SILENT:
            if (self.PRINT_DETAILS or self.PRINT_SUMMARIES):
                print(" ")
                print("STATS TEST:")

        opt = FireGirlPolicyOptimizer()
        opt.SILENT = True
        opt.createFireGirlPathways(pathway_count, years, start_ID)

        #running stat functions
        sup_costs = suppression_cost_stats_by_year(opt.pathway_set)
        harvests = timber_harvest_stats_by_year(opt.pathway_set)
        growth = growth_stats_by_year(opt.pathway_set)
        fires = fire_stats_by_year(opt.pathway_set)


        if not self.SILENT:
            if self.PRINT_DETAILS:
                print("Suppression Cost Stats")
                print("ave, max, min, std, 95%high, 95%low")
                for i in range(len(sup_costs[0])):
                    #suppresion_cost_stats_by_year returns 6 lists
                    for j in range(6):
                        print(str(sup_costs[j][i]) + ","), #comma tells python not to end the line
                    #now end the line
                    print(" ")

                print(" ")
                print("Harvest Value Stats")
                print("ave, max, min, std, 95%high, 95%low")
                for i in range(len(harvests[0])):
                    #timber_harvest_stats_by_year returns 6 lists
                    for j in range(6):
                        print(str(harvests[j][i]) + ","), #comma tells python not to end the line
                    #now end the line
                    print(" ")

                print(" ")
                print("Timber Growth Stats")
                print("ave, max, min, std, 95%high, 95%low")
                for i in range(len(growth[0])):
                    #growth_stats_by_year returns 6 lists
                    for j in range(6):
                        print(str(growth[j][i]) + ","), #comma tells python not to end the line
                    #now end the line
                    print(" ")

                print(" ")
                print("Fire Stats:")
                print("Cells Burned, , , , , , Timber Lost, , , , , , Suppress Decisions")
                print("ave, max, min, std, 95%high, 95%low, ave, max, min, std, 95%high, 95%low")
                for i in range(len(fires[0][0])):
                    #fire_stats_by_year returns 3 lists
                    # the first is a sub-list of 6 stats for CELLS BURNED, as the features above

                    #printing Cells burned stats
                    for j in range(6):
                        print(str(fires[0][j][i]) + ","), #comma tells python not to end the line
                    #printing timber lost stats
                    for j in range(6):
                        print(str(fires[1][j][i]) + ","), #comma tells python not to end the line
                    #printing suppress decisions stat and ending the line
                    print(str(fires[2][i]))

    def monte_carlo_baselines(self, pathway_count=5, years=100, start_ID=2000):
        #This test will roll out N pathways using a let-burn, suppress-all, and coin-toss policies

        if not self.SILENT:
            if (self.PRINT_DETAILS or self.PRINT_SUMMARIES):
                print(" ")
                print("MONTE CARLO BASELINES:")

        opt = FireGirlPolicyOptimizer()
        pol = FireGirlPolicy()
        opt.SILENT = True


        #setting a let-burn policy
        pol.setLetBurn()

        net_val_sum = 0.0

        #doing let-burn pathways
        if not self.SILENT:
            if self.PRINT_DETAILS:
                print("--beginning let-burn pathway generation")

        for pw in range(pathway_count):
            opt.createFireGirlPathways(1, years, start_ID+pw, pol)
            #accessing the pathway's net value member directly
            net_val_sum += opt.pathway_set[0].net_value

        #calculate the average net value for all let-burn pathways
        ave_let_burn = net_val_sum / pathway_count

        #reset the sum for the next test
        net_val_sum = 0.0




        #setting a suppress-all policy
        pol.setSuppressAll()

        if not self.SILENT:
            if self.PRINT_DETAILS:
                print("--beginning suppress-all pathway generation")

        #doing suppress-all pathways
        for pw in range(pathway_count):
            opt.createFireGirlPathways(1, years, start_ID+pw, pol)
            #accessing the pathway's net value member directly
            net_val_sum += opt.pathway_set[0].net_value

        #calculate the average net value for all let-burn pathways
        ave_suppress_all = net_val_sum / pathway_count

        #reset the sum for the next test
        net_val_sum = 0.0




        #setting a coin-toss policy (all params = 0)
        pol.setParams([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

        if not self.SILENT:
            if self.PRINT_DETAILS:
                print("--beginning coin-toss pathway generation")

        #doing coin-toss pathways
        for pw in range(pathway_count):
            opt.createFireGirlPathways(1, years, start_ID+pw, pol)
            #accessing the pathway's net value member directly
            net_val_sum += opt.pathway_set[0].net_value

        #calculate the average net value for all let-burn pathways
        ave_coin_toss = net_val_sum / pathway_count


        if not self.SILENT:
            if (self.PRINT_DETAILS or self.PRINT_SUMMARIES):
                #printing summary information
                print(" ")
                print("Average Net Value of:")
                print("  let-burn pathways:     " + str(round(ave_let_burn)))
                print("  suppress-all pathways: " + str(round(ave_suppress_all)))
                print("  coin-toss pathways:    " + str(round(ave_coin_toss)))

            if self.PRINT_DETAILS:
                #printing details
                print("Test Details:")
                print("  Pathway Count: " + str(pathway_count))
                print("  Years/Pathway: " + str(years))
                print("  Pathway Start ID: " + str(start_ID))


        return [ave_let_burn, ave_suppress_all, ave_coin_toss]

class FireGirlTrials:
    """This class contains member functions that produce test data as outputs, replacing test scripts

    """

    def __init__(self):
        """Initialization function: Instantiates a FireGirlPolicyOptimizer and FireGirlPolicy for trials to use.

        """
        self.Opt = FireGirlPolicyOptimizer()
        self.Policy = FireGirlPolicy()

    def policy_comparisons_1(self, pathway_count=75, years=100, start_ID=2000):
        """Runs the same N pathways on several different policies and prints stats for each

        Arguements
        -pathway_count: the number of pathways to run under each policy
        -years: how many years each pathway should run
        -start_ID: which pathway ID to assign to the first pathway in each set. Subsequent pathway IDs 
        increment by one

        Return
        None. Results are printed to file (there's a lot of them)

        """

        #Create N pathways under let-burn
        self.Policy.setLetBurn()
        self.Opt.setPolicy(self.Policy)
        self.Opt.createFireGirlPathways(pathway_count,years,start_ID)
        stats_let_burn = all_stats_by_year(self.Opt.pathway_set)
        #copy pathway net values
        vals_let_burn = self.Opt.getNetValues()
        
        #Create N pathways under suppress-all
        self.Policy.setSuppressAll()
        self.Opt.setPolicy(self.Policy)
        self.Opt.createFireGirlPathways(pathway_count,years,start_ID)
        stats_suppress_all = all_stats_by_year(self.Opt.pathway_set)
        #copy pathway net values
        vals_suppress_all = self.Opt.getNetValues()

        #Create N pathways under coin-toss
        self.Policy.setParams([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        self.Opt.setPolicy(self.Policy)
        self.Opt.createFireGirlPathways(pathway_count,years,start_ID)
        stats_coin_toss = all_stats_by_year(self.Opt.pathway_set)
        #copy pathway net values
        vals_coin_toss = self.Opt.getNetValues()

        #Create N pathways under previously found J1.1 policy
        self.Policy.setParams([-4.0548126597150898, 4.0548126597150898, 4.0548126597150898, -4.0548126597150898, 4.0548126597150898, -2.216996097452042, -2.216996097452042, -2.216996097452042, -2.216996097452042, -2.216996097452042, -2.216996097452042])
        self.Opt.setPolicy(self.Policy)
        self.Opt.createFireGirlPathways(pathway_count,years,start_ID)
        stats_J1_1 = all_stats_by_year(self.Opt.pathway_set)
        #copy pathway net values
        vals_J1_1 = self.Opt.getNetValues()

        #Create N pathways under previously found J2 policy
        self.Policy.setParams([-8.8497603806694123, 10.0, 0.14475050808112244, -10.0, 8.7811621637830832, 4.5530784623219773, 7.6456981485587256, 4.3894187002736862, 6.6923034115234064, -0.88238815750515465, 10.0])
        self.Opt.setPolicy(self.Policy)
        self.Opt.createFireGirlPathways(pathway_count,years,start_ID)
        stats_J2 = all_stats_by_year(self.Opt.pathway_set)
        #copy pathway net values
        vals_J2 = self.Opt.getNetValues()


        #open the output file
        f = open('TrialResult-PolicyComparisons1.txt', 'w')


        f.write("FireGirlTrials_PolicyComparisons_1 Outputs\n")
        f.write("\n")
        f.write("\n")
        
        #write let-burn statistics
        f.write("PATHWAYS GENERATED UNDER a LET-BURN POLICY\n")
        #printing column labels for excel, etc...
        f.write("supp_ave,supp_min,supp_max,supp_std,supp_95_low,supp_95_high,")
        f.write("harv_ave,harv_min,harv_max,harv_std,harv_95_low,harv_95_high,")
        f.write("grwth_ave,grwth_min,grwth_max,grwth_std,grwth_95_low,grwth_95_high,")
        f.write("cells_burned_ave,cells_burned_min,cells_burned_max,cells_burned_std,cells_burned_95_low,cells_burned_95_high,")
        f.write("timb_lost_ave,timb_lost_min,timb_lost_max,timb_lost_std,timb_lost_95_low,timb_lost_95_high,")
        f.write("supp_decicions\n")

        #new row for each year
        for y in range(years):
            #print suppression cost stats for this year
            #the first element of stats_whatever is a string decription
            #element 1 is the suppression costs (6 lists)
            for i in range(6):
                f.write(str(round(stats_let_burn[1][i][y], 3)) + ",")

            #print harvest stats for this year
            #element 2 of stats_whatever is harvest values (6 lists)
            for i in range(6):
                f.write(str(round(stats_let_burn[2][i][y], 3)) + ",")

            #print growth stats for this year
            #element 3 of stats_whatever is growth  (6 lists)
            for i in range(6):
                f.write(str(round(stats_let_burn[3][i][y], 3)) + ",")

            #print fire stats for this year
            #element 4 of stats_whatever is fire
            for i in range(6):
                #element 0 of fire is cells burned (6 lists)
                f.write(str(round(stats_let_burn[4][0][i][y], 3)) + ",")

            for i in range(6):
                #element 1 of fire is timber lost (6 lists)
                f.write(str(round(stats_let_burn[4][1][i][y], 3)) + ",")

            #element 2 of fire is suppress decisions (1 list)
            f.write(str(round(stats_let_burn[4][2][y], 3)) + "\n") #this also ends the line before next year's stats begin writing
            

        f.write("\n")
        f.write("\n")

        #write suppress-all statistics
        f.write("PATHWAYS GENERATED UNDER a SUPPRESS-ALL POLICY\n")
        #printing column labels for excel, etc...
        f.write("supp_ave,supp_min,supp_max,supp_std,supp_95_low,supp_95_high,")
        f.write("harv_ave,harv_min,harv_max,harv_std,harv_95_low,harv_95_high,")
        f.write("grwth_ave,grwth_min,grwth_max,grwth_std,grwth_95_low,grwth_95_high,")
        f.write("cells_burned_ave,cells_burned_min,cells_burned_max,cells_burned_std,cells_burned_95_low,cells_burned_95_high,")
        f.write("timb_lost_ave,timb_lost_min,timb_lost_max,timb_lost_std,timb_lost_95_low,timb_lost_95_high,")
        f.write("supp_decicions\n")

        #new row for each year
        for y in range(years):
            #print suppression cost stats for this year
            #the first element of stats_whatever is a string decription
            #element 1 is the suppression costs (6 lists)
            for i in range(6):
                f.write(str(round(stats_suppress_all[1][i][y], 3)) + ",")

            #print harvest stats for this year
            #element 2 of stats_whatever is harvest values (6 lists)
            for i in range(6):
                f.write(str(round(stats_suppress_all[2][i][y], 3)) + ",")

            #print growth stats for this year
            #element 3 of stats_whatever is growth  (6 lists)
            for i in range(6):
                f.write(str(round(stats_suppress_all[3][i][y], 3)) + ",")

            #print fire stats for this year
            #element 4 of stats_whatever is fire
            for i in range(6):
                #element 0 of fire is cells burned (6 lists)
                f.write(str(round(stats_suppress_all[4][0][i][y], 3)) + ",")

            for i in range(6):
                #element 1 of fire is timber lost (6 lists)
                f.write(str(round(stats_suppress_all[4][1][i][y], 3)) + ",")

            #element 2 of fire is suppress decisions (1 list)
            f.write(str(round(stats_suppress_all[4][2][y], 3)) + "\n") #this also ends the line before next year's stats begin writing

        f.write("\n")
        f.write("\n")


        #write coin-toss statistics
        f.write("PATHWAYS GENERATED UNDER a COIN-TOSS POLICY\n")

        #printing column labels for excel, etc...
        f.write("supp_ave,supp_min,supp_max,supp_std,supp_95_low,supp_95_high,")
        f.write("harv_ave,harv_min,harv_max,harv_std,harv_95_low,harv_95_high,")
        f.write("grwth_ave,grwth_min,grwth_max,grwth_std,grwth_95_low,grwth_95_high,")
        f.write("cells_burned_ave,cells_burned_min,cells_burned_max,cells_burned_std,cells_burned_95_low,cells_burned_95_high,")
        f.write("timb_lost_ave,timb_lost_min,timb_lost_max,timb_lost_std,timb_lost_95_low,timb_lost_95_high,")
        f.write("supp_decicions\n")

        #new row for each year
        for y in range(years):
            #print suppression cost stats for this year
            #the first element of stats_whatever is a string decription
            #element 1 is the suppression costs (6 lists)
            for i in range(6):
                f.write(str(round(stats_coin_toss[1][i][y], 3)) + ",")

            #print harvest stats for this year
            #element 2 of stats_whatever is harvest values (6 lists)
            for i in range(6):
                f.write(str(round(stats_coin_toss[2][i][y], 3)) + ",")

            #print growth stats for this year
            #element 3 of stats_whatever is growth  (6 lists)
            for i in range(6):
                f.write(str(round(stats_coin_toss[3][i][y], 3)) + ",")

            #print fire stats for this year
            #element 4 of stats_whatever is fire
            for i in range(6):
                #element 0 of fire is cells burned (6 lists)
                f.write(str(round(stats_coin_toss[4][0][i][y], 3)) + ",")

            for i in range(6):
                #element 1 of fire is timber lost (6 lists)
                f.write(str(round(stats_coin_toss[4][1][i][y], 3)) + ",")

            #element 2 of fire is suppress decisions (1 list)
            f.write(str(round(stats_coin_toss[4][2][y], 3)) + "\n") #this also ends the line before next year's stats begin writing

        f.write("\n")
        f.write("\n")

        #write J1.1 statistics
        f.write("PATHWAYS GENERATED UNDER a J1.1 POLICY\n")

        #printing column labels for excel, etc...
        f.write("supp_ave,supp_min,supp_max,supp_std,supp_95_low,supp_95_high,")
        f.write("harv_ave,harv_min,harv_max,harv_std,harv_95_low,harv_95_high,")
        f.write("grwth_ave,grwth_min,grwth_max,grwth_std,grwth_95_low,grwth_95_high,")
        f.write("cells_burned_ave,cells_burned_min,cells_burned_max,cells_burned_std,cells_burned_95_low,cells_burned_95_high,")
        f.write("timb_lost_ave,timb_lost_min,timb_lost_max,timb_lost_std,timb_lost_95_low,timb_lost_95_high,")
        f.write("supp_decicions\n")

        #new row for each year
        for y in range(years):
            #print suppression cost stats for this year
            #the first element of stats_whatever is a string decription
            #element 1 is the suppression costs (6 lists)
            for i in range(6):
                f.write(str(round(stats_J1_1[1][i][y], 3)) + ",")

            #print harvest stats for this year
            #element 2 of stats_whatever is harvest values (6 lists)
            for i in range(6):
                f.write(str(round(stats_J1_1[2][i][y], 3)) + ",")

            #print growth stats for this year
            #element 3 of stats_whatever is growth  (6 lists)
            for i in range(6):
                f.write(str(round(stats_J1_1[3][i][y], 3)) + ",")

            #print fire stats for this year
            #element 4 of stats_whatever is fire
            for i in range(6):
                #element 0 of fire is cells burned (6 lists)
                f.write(str(round(stats_J1_1[4][0][i][y], 3)) + ",")

            for i in range(6):
                #element 1 of fire is timber lost (6 lists)
                f.write(str(round(stats_J1_1[4][1][i][y], 3)) + ",")

            #element 2 of fire is suppress decisions (1 list)
            f.write(str(round(stats_J1_1[4][2][y], 3)) + "\n") #this also ends the line before next year's stats begin writing


        f.write("\n")
        f.write("\n")

        #write J2 statistics
        f.write("PATHWAYS GENERATED UNDER a J2 POLICY\n")

        #printing column labels for excel, etc...
        f.write("supp_ave,supp_min,supp_max,supp_std,supp_95_low,supp_95_high,")
        f.write("harv_ave,harv_min,harv_max,harv_std,harv_95_low,harv_95_high,")
        f.write("grwth_ave,grwth_min,grwth_max,grwth_std,grwth_95_low,grwth_95_high,")
        f.write("cells_burned_ave,cells_burned_min,cells_burned_max,cells_burned_std,cells_burned_95_low,cells_burned_95_high,")
        f.write("timb_lost_ave,timb_lost_min,timb_lost_max,timb_lost_std,timb_lost_95_low,timb_lost_95_high,")
        f.write("supp_decicions\n")

        #new row for each year
        for y in range(years):
            #print suppression cost stats for this year
            #the first element of stats_whatever is a string decription
            #element 1 is the suppression costs (6 lists)
            for i in range(6):
                f.write(str(round(stats_J2[1][i][y], 3)) + ",")

            #print harvest stats for this year
            #element 2 of stats_whatever is harvest values (6 lists)
            for i in range(6):
                f.write(str(round(stats_J2[2][i][y], 3)) + ",")

            #print growth stats for this year
            #element 3 of stats_whatever is growth  (6 lists)
            for i in range(6):
                f.write(str(round(stats_J2[3][i][y], 3)) + ",")

            #print fire stats for this year
            #element 4 of stats_whatever is fire
            for i in range(6):
                #element 0 of fire is cells burned (6 lists)
                f.write(str(round(stats_J2[4][0][i][y], 3)) + ",")

            for i in range(6):
                #element 1 of fire is timber lost (6 lists)
                f.write(str(round(stats_J2[4][1][i][y], 3)) + ",")

            #element 2 of fire is suppress decisions (1 list)
            f.write(str(round(stats_J2[4][2][y], 3)) + "\n") #this also ends the line before next year's stats begin writing



        #write pathway net values
        f.write("\n\nPATHWAY NET VALUES")
        f.write("\nLet-Burn Pathways,")
        for i in range(pathway_count):
            f.write(  str(round((vals_let_burn[i]),3) )  + ",")
        f.write("\nSuppress-All Pathways,")
        for i in range(pathway_count):
            f.write(  str(round((vals_suppress_all[i]),3) )  + ",")
        f.write("\nCoin-Toss Pathways,")
        for i in range(pathway_count):
            f.write(  str(round((vals_coin_toss[i]),3) )  + ",")
        f.write("\nJ1.1 Pathways,")
        for i in range(pathway_count):
            f.write(  str(round((vals_J1_1[i]),3) )  + ",")
        f.write("\nJ2 Pathways,")
        for i in range(pathway_count):
            f.write(  str(round((vals_J2[i]),3) )  + ",")

        #write Averages
        f.write("\n\nAVERAGE NET VALUES") 
        f.write("\nLet-Burn Pathways," +     str(round(mean(vals_let_burn)))  )
        f.write("\nSuppress-All Pathways," + str(round(mean(vals_suppress_all)))  )
        f.write("\nCoin-Toss Pathways," +    str(round(mean(vals_coin_toss)))  )
        f.write("\nJ1.1 Pathways," +         str(round(mean(vals_J1_1)))  )
        f.write("\nJ2 Pathways," +           str(round(mean(vals_J2)))  )




        #close the output file
        f.close()







#setting up service-style tests. This will activate if you issue: "python FireGirlTests.py" at a command line, but
#  will otherwise be ignored
if __name__ == "__main__":


    tests = FireGirlTests()
    #tests.SILENT = True
    tests.PRINT_DETAILS = False
    tests.PRINT_SUMMARIES = True

    #running monte carlo tests, and ignoring results (at the moment)
    tests.monte_carlo_baselines()


    #finished
    print(" ")
    print(" ")
    print("All Tests Complete")
