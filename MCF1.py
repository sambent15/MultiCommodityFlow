from __future__ import print_function
import string
from ortools.graph import pywrapgraph

#Shortest Path dep / arr / cout / filtre
# 1 source -1 en dest pour offre pour que le solveur trouve le shortest path

def main():
    arc_depart = [0, 0, 1, 1, 1, 2, 2, 3, 4]
    arc_arrivee = [1, 2, 2, 3, 4, 3, 4, 4, 2]
    cout = [4, 4, 2, 2, 6, 1, 3, 2, 3]
    capa = [15, 8, 20, 4, 10, 15, 4, 20, 5]

    offre = [20, 0, 0, -5, -15]

    min_cost_flow = pywrapgraph.SimpleMinCostFlow()

    for i in range(0, len(arc_depart)):
        min_cost_flow.AddArcWithCapacityAndUnitCost(arc_depart[i], arc_arrivee[i],
                                                    capa[i], cout[i])

    for i in range(0, len(offre)):
        min_cost_flow.SetNodeSupply(i, offre[i])

        # Find the minimum cost flow between node 0 and node 4.
    if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
        print('Le cout optimal est :', min_cost_flow.OptimalCost())
        print('  Arc    Flot / Capacité  Cout')
        for i in range(min_cost_flow.NumArcs()):
            debutArc = string.ascii_uppercase[min_cost_flow.Tail(i)]
            finArc = string.ascii_uppercase[min_cost_flow.Head(i)]
            flot = min_cost_flow.Flow(i)
            capacite = min_cost_flow.Capacity(i)
            cost = flot * min_cost_flow.UnitCost(i)
            print('%1s -> %1s   %3s  / %3s       %3s' % (
                debutArc,
                finArc,
                flot,
                capacite,
                cost))
    else:
        print('Probleme')


if __name__ == '__main__':
    main()
