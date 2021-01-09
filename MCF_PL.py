import time
import Graph_Tools as gt
from ortools.linear_solver import pywraplp
import numpy as np

np.random.seed(1) # Permet de figer la graine afin d'avoir toujours la même instance

def multicommodityflow_pl(graph, demands, cost=None):
    n = len(graph)
    arcs = []
    # ARCS DU GRAPH :
    for i in range(n):
        for j in range(n):
            if (graph[i][j] > 0):
                arcs.append([i, j])

    # CAPACITE DE CES ARCS
    capa = []
    m = len(arcs)
    for i in range(m):
        capa.append(graph[arcs[i][0]][arcs[i][1]])


    k = len(demands)    # NB DE DEMANDES

    # Solveur google avec backend SCIP (Solving Constraint Integer Programs) : en nb entiers
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # On crée une variable binaire = 1(TRUE) si arc a est utilisé par demande k. SINON 0(FALSE)
    X = []
    for i in range(m):
        aux = []
        for j in range(k):
            aux.append(solver.IntVar(0, 1, 'x_' + str(arcs[i][0]) + "_" + str(arcs[i][1]) + "_" + str(j + 1)))
        X.append(aux)

    # On crée une variable binaire = 1(TRUE) s'il y a flot total i de l'arc a. SINON 0(FALSE)
    C = []
    for a in range(m):
        aux = []
        for i in range(capa[a] + 1):
            aux.append(solver.IntVar(0, 1, 'C_' + str(arcs[a][0]) + "_" + str(arcs[a][1]) + "_" + str(i)))
        C.append(aux)

    # CONTRAINTE 1 : Unique resulting flow
    contr_resultingflow = []
    for a in range(m):
        aux = solver.Constraint(1, 1, 'contr_resultingflow_' + str(a + 1))
        contr_resultingflow.append(aux)
    for a in range(m): ##pour chaque arc
        for i in range(capa[a] + 1):
            contr_resultingflow[a].SetCoefficient(C[a][i], 1)

    # CONTRAINTE 2 : flow conservation
    contr_flowconserv = []
    for u in range(n): #u node
        aux = []
        for i in range(k): # k demand
            if u == demands[i][0]:  # u = sk
                aux.append(solver.Constraint(1, 1, 'contr_flowconserv_' + str(a + 1)))
            elif u == demands[i][1]:  # u = tk
                aux.append(solver.Constraint(-1, -1, 'contr_flowconserv_' + str(a + 1)))
            else:
                aux.append(solver.Constraint(0, 0, 'contr_flowconserv_' + str(a + 1)))
        contr_flowconserv.append(aux)
    for a in range(m):
        for i in range(k):
            u = arcs[a][0]
            v = arcs[a][1]
            contr_flowconserv[u][i].SetCoefficient(X[a][i], +1)
            contr_flowconserv[v][i].SetCoefficient(X[a][i], -1)

    # CONTRAINTE 3 : capacity
    contr_capa = []
    for a in range(m):
        aux = solver.Constraint(- solver.infinity(), 0, 'contr_capa_' + str(a + 1))
        contr_capa.append(aux)
    for a in range(m): #for each edge (arc)
        for i in range(capa[a] + 1):
            contr_capa[a].SetCoefficient(C[a][i], -i)
    for a in range(m):
        for i in range(k): #for each demand (k)
            contr_capa[a].SetCoefficient(X[a][i], demands[i][2])

    objective = solver.Objective()

    # Cout au carré
    for a in range(m):
        for i in range(capa[a] + 1):
            if cost is None: # SI on ne donne pas de cout, on met le coeff au carré
                objective.SetCoefficient(C[a][i], i ** 2)
            else: #Si on en met, on s'assure que le coef soit au carré
                objective.SetCoefficient(C[a][i], int(i ** 2) * int(cost[arcs[a][0]][arcs[a][1]]))

    objective.SetMinimization() # On dit au solveur qu'on veut minimiser le cout total
    start_time = time.time()    # On initialise l'heure dans le but de calculer le temps d'execution
    solver.Solve()          #ON RESOUD !!!! Merci ORTools
    temps = time.time() - start_time    # On calcule le temps d'execution

    for i in range(k):
        for a in range(m):
            if (X[a][i].solution_value() > 1e-6):
                # 1e-6 car  certaines approx sont tres petites (erreurs d'approx) donc on les vire
                print("Demande # %3s || Passe par l'arc : %1s -> %1s" % (str(i + 1), str(arcs[a][0]), str(arcs[a][1])))

    for a in range(m):
        for i in range(capa[a] + 1):
            if (C[a][i].solution_value() > 1e-6 and i > 0):  # Matrice avec plein de 0, on les ignore :
                print("Arc %1s -> %1s || Flot total = %3s" % (str(arcs[a][0]), str(arcs[a][1]), str(i)))
    return round(objective.Value(), 3), round(temps, 3)


if __name__ == '__main__':
    # taille du graphe en nombre de sommets
    n = 20  # nombre de sommets
    m = 150  # nombre de liens
    k = 10  # nombre de demandes
    #### CREATION DU GRAPHE ####
    graph = gt.generateGraph(n, m)
    cost = gt.generateCosts(graph)
    demands = gt.generateDemands(k, n)
    print("Les demandes générées sont :", demands)
    # Multi Commodity Flow
    MCF = multicommodityflow_pl(graph, demands)
    print("Le Problème du Multi Commodity Flow a été résolu via PL avec un coût total de ", MCF[0],
          "et un temps d'exécution de ", MCF[1], "secondes")
