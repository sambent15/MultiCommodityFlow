import sys
import time
from glouton import greedyMCMC
from fastapproximate import fastApproxMCMC
#network=greedyMCMC()
#unit test1 : read
#network.readGraph(sys.argv[1])
#network.printGraph()
#unit test 2: queryPath
#network.queryPath(network.requirements)
#fastmcmc=fastApproxMCMC()
#fastmcmc.readGraph(sys.argv[1])
#fastmcmc.printGraph()
#start = time.time()
#fastmcmc.fastApproximation(fastmcmc.requirements,0.1,1000)
#print "it took", time.time() - start, "seconds."


network=greedyMCMC()
#unit test1 : read
network.readGraph("graph/5.net")
#network.printGraph()
#unit test 2: queryPath
start = time.time()
network.greedy(network.requirements)
print("ça a pris", time.time() - start, "secondes.")