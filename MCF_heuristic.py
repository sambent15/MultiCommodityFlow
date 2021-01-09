import sys
import copy
from edge import Edge
from min_cost_flow import MinCostFlow
import time


arglenth = len(sys.argv)

def greedy(self, listofpairs):
    print("len(listofpairs): %s" % (len(listofpairs)))
    sop = set()
    for p in listofpairs:
        sop.add((p[0], p[1]))
    print("len(setofpairs): %s" % (len(sop)))

    solutions = {}
    e_pair = {}
    cur = 0
    start_time = time.time()  # On initialise l'heure dans le but de calculer le temps d'execution
    while (len(solutions) < len(listofpairs)):
        for pair in listofpairs:
            print("%s < %s" % (len(solutions), len(listofpairs)))
            cur += 1
            print(cur)
            if (pair[0], pair[1]) in solutions:
                continue
            # the flow with residual graph
            flow = MinCostFlow.minCostFlow(pair[0], pair[1], pair[2], self.alledges, False)
            cost = sum([link[0].getAVLDualL() * link[1] for link in flow])
            # the flow with original graph
            if len(flow) > 0:
                newflow = MinCostFlow.minCostFlow(pair[0], pair[1], pair[2], self.alledges, True)
                newcost = sum([link[0].getAVLDualL() * link[1] for link in newflow])
                if (float(cost) / float(newcost) > 1.5):
                    for link in newflow:
                        if link[0].getAVLBW() < link[1]:
                            link[0].extendBeta(3)
                            for p in e_pair[link[0]]:
                                sol = solutions.pop(p)
                                for ec in sol:
                                    ec[0].avlBW += ec[1]
                                    if ec[0] != link[0]:
                                        e_pair[ec[0]].remove(p)
                            e_pair[link[0]] = set()
                else:
                    solutions[(pair[0], pair[1])] = flow
                    for link in flow:
                        link[0].useBW(link[1])
                        if link[0] in e_pair:
                            s = e_pair[link[0]]
                            s.add((pair[0], pair[1]))
                        else:
                            s = set()
                            s.add((pair[0], pair[1]))
                            e_pair[link[0]] = s
            else:
                newflow = MinCostFlow.minCostFlow(pair[0], pair[1], pair[2], self.alledges, True)
                for link in newflow:
                    if link[0].getAVLBW() < link[1]:
                        link[0].extendBeta(3)
                        for p in e_pair[link[0]]:
                            sol = solutions.pop(p)
                            for ec in sol:
                                ec[0].avlBW += ec[1]
                                if ec[0] != link[0]:
                                    e_pair[ec[0]].remove(p)
                        e_pair[link[0]] = set()
        for pair in solutions:
            print(str(pair))
            sol = solutions[pair]
            self.printFlow(sol)
        if len(solutions) == len(listofpairs):
            print("reussi apres %s iterations" % (cur))
            print("nombre de sommets: %s" % (len(self.alledges)))
            print("nombre de demandes: %s " % (len(listofpairs)))
            print("nombre de liens: %s " % (self.numV))
            usedbw = self.usedBW(solutions)
            cost = sum([k.cost * usedbw[k] for k in usedbw])
            print("cout total:  %s" % (cost))
            print("capa max  %s" % (self.maxCapacity))
        else:
            print("echec apres %s iterations" % (cur))
    temps = time.time() - start_time  # On calcule le temps d'execution
    return cost, temps