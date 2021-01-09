import networkx as nx
import sys

class MinCostFlow:
  @staticmethod
  def minCostFlow(src,dst,bw,edges,all=False,factor=1):
    G = nx.DiGraph()
    G.add_node(src, demand = bw)
    G.add_node(dst, demand = -bw)
    vtoe={}
    res=[]
    for e in edges:
      if(e.getAVLBW(all)>0):
        G.add_edge(e.v1, e.v2, weight = int((e.cost+e.beta)/factor), capacity = e.getAVLBW(all))
        G.add_edge(e.v2, e.v1, weight = int((e.cost+e.beta)/factor), capacity = e.getAVLBW(all))
        vtoe[(e.v1,e.v2)]=e
        vtoe[(e.v2,e.v1)]=e
    try:
        flowDict = nx.min_cost_flow(G)
        for k in flowDict:
            for j in flowDict[k]:
                if flowDict[k][j]>0:
                    res.append([vtoe[(k,j)],flowDict[k][j]])
    except nx.exception.NetworkXUnfeasible:
      print("Pas de flot realisable")
    return res