import Graph_Tools as gt
import MCF_PL as pl
import MCF_heuristic as hrstc
import MCF_delay as dl
from ortools.linear_solver import pywraplp


# taille du graphe en nombre de sommets
n = 40  # nombre de sommets
m = 284  # nombre de liens
k = 39  # nombre de demandes
    #### CREATION DU GRAPHE ####
graph = gt.generateGraph(n, m)
cost = gt.generateCosts(graph)
demands = gt.generateDemands(k, n)
print("Les demandes générées sont :", demands)
# Multi Commodity Flow PL
MCF = pl.multicommodityflow_pl(graph, demands)
print("Le Problème du Multi Commodity Flow a été résolu via PL avec un coût total de ", MCF[0],
      "et un temps d'exécution de ", MCF[1], "secondes")

# Multi Commodity Flow Heuristic
MCFGlouton= hrstc.greedy(graph, demands)
print("Le Problème du Multi Commodity Flow a été résolu via notre heuristique avec un coût total de ", MCFGlouton[0],
      "et un temps d'exécution de ", MCFGlouton[1], "secondes")

# MCF CONGESTION
print("Traitons maintenant la congestion :")
MCFDelay = dl.decongestion(graph, demands)
print("cout : ", MCFDelay[0])
print("temps =", MCFDelay[1], "secondes")