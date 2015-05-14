import cProfile, pstats, StringIO
from FireGirlOptimizer import *

class FireGirlProfiler:

    def __init__(self):
        pass

    def createPathways(self):

        opt = FireGirlPolicyOptimizer()

        pr = cProfile.Profile()
        pr.enable()

        opt.createFireGirlPathways(20,100)

        pr.disable()

        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()



if __name__ == "__main__":
    profiler = FireGirlProfiler()
    profiler.createPathways()
