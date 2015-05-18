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
    
    def testListBuilding(self):
        pr = cProfile.Profile()
        pr.enable()
        for i in range(1000):
            self.listBuilding_Append()
            self.listBuilding_Copy()
        pr.disable()

        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()
    
    def listBuilding_Append(self):
    
        width = 129
        height = 129
        l = []
        for i in range(width):
            l.append([])
            for j in range(height):
                l[i].append(0)
    
    def listBuilding_Copy(self):
        width = 129
        height = 129
        inner = [0] * height
        l = [inner] * width





if __name__ == "__main__":
    profiler = FireGirlProfiler()
    profiler.createPathways()
