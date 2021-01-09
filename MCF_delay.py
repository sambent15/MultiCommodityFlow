import time
from ortools.linear_solver import pywraplp
import numpy as np


def decongestion(graph, demands):
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

    k = len(demands)  # NB DE DEMANDES

    # Solveur google avec backend SCIP (Solving Constraint Integer Programs) : en nb entiers
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # On crée une variable binaire = 1(TRUE) si arc a est utilisé par demande k. SINON 0(FALSE)
    X = []
    for i in range(m):
        use = []
        for j in range(k):
            use.append(solver.IntVar(0, 1, 'x_' + str(arcs[i][0]) + "_" + str(arcs[i][1]) + "_" + str(j + 1)))
        X.append(use)

    Z = []
    for a in range(m):
        Z.append(solver.NumVar(0, 1, 'z_' + str(a + 1)))

    # CONTRAINTE 3 : capacity
    contr_capa = []
    for a in range(m):
        aux = solver.Constraint(0, 0, 'contr_capa_' + str(a + 1))
        contr_capa.append(aux)
    for a in range(m):
        contr_capa[a].SetCoefficient(Z[a], -int(capa[a]))
        for i in range(k):
            contr_capa[a].SetCoefficient(X[a][i], demands[i][2])

    # CONTRAINTE 2 : flow conservation
    contr_flowconserv = []

    # pour noeud u et demande k
    for u in range(n):
        aux = []
        for i in range(k):
            if u == demands[i][0]:  # u = sk
                aux.append(solver.Constraint(1, 1, 'contr_flowconserv_' + str(a + 1)))
            elif u == demands[i][1]:  # u = tk
                aux.append(solver.Constraint(-1, -1, 'contr_flowconserv_' + str(a + 1)))
            else:  # sinon
                aux.append(solver.Constraint(0, 0, 'contr_flowconserv_' + str(a + 1)))
        contr_flowconserv.append(aux)

    for a in range(m):
        for i in range(k):
            u = arcs[a][0]
            v = arcs[a][1]
            contr_flowconserv[u][i].SetCoefficient(X[a][i], +1)
            contr_flowconserv[v][i].SetCoefficient(X[a][i], -1)

    objective = solver.Objective()  # On dit au solveur qu'on veut minimiser le cout total

    for a in range(m):
        objective.SetCoefficient(Z[a], 1 / m)  # On passe a linverse le coeff dapres la formule donnée
    objective.SetMinimization()

    start_time = time.time()
    solver.Solve()
    temps = time.time() - start_time

    decong = []
    for a in range(m):
        if Z[a].solution_value() > 1e-6:
            decong.append(Z[a].solution_value())
        else:
            decong.append(0)

    decong_final = 0
    for a in range(m):
        decong_final += 1 / ((1 - decong[a]) * capa[a])

    return round(decong_final, 2), round(temps, 3)
