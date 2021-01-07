def prog_lin_1(graph, demands, cost=None, afficher=True):
    n = len(graph)

    arcs = get_arcs(graph)

    m = len(arcs)

    capa = get_capa(graph)

    k = len(demands)

    # Create the linear solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Ici on va creer les variables X[a][k] de façon que
    # X[a][k] = 1 si l'arc a est utilisé par la demande k et 0 sinon
    X = []
    for i in range(m):
        aux = []
        for j in range(k):
            aux.append(solver.IntVar(0, 1, 'x_' + str(arcs[i][0]) + "" + str(arcs[i][1]) + "" + str(j + 1)))
        X.append(aux)

    # Ici on va créer des constraints pour respecter les capacités.
    ct1 = []
    for a in range(m):
        aux = solver.Constraint(0, int(capa[a]), 'ct1_' + str(a + 1))
        ct1.append(aux)

    ##pour chaque arc
    for a in range(m):
        for i in range(k):
            ct1[a].SetCoefficient(X[a][i], demands[i][2])

    # Ici on va créer les constraint de la conservation de flot
    ct2 = []

    # pour noeud u et demande k
    for u in range(n):
        aux = []
        for i in range(k):
            if u == demands[i][0]:  # u = sk
                aux.append(solver.Constraint(1, 1, 'ct2_' + str(a + 1)))
            elif u == demands[i][1]:  # u = tk
                aux.append(solver.Constraint(-1, -1, 'ct2_' + str(a + 1)))
            else:  # sinon
                aux.append(solver.Constraint(0, 0, 'ct2_' + str(a + 1)))
        ct2.append(aux)

    for a in range(m):
        for i in range(k):
            u = arcs[a][0]
            v = arcs[a][1]
            ct2[u][i].SetCoefficient(X[a][i], +1)
            ct2[v][i].SetCoefficient(X[a][i], -1)

    # Ici on va poser l'objective de minimiser le cout total
    objective = solver.Objective()
    for a in range(m):
        for i in range(k):
            if cost is None:
                objective.SetCoefficient(X[a][i], demands[i][2])
            else:
                objective.SetCoefficient(X[a][i], int(demands[i][2]) * int(cost[arcs[a][0]][arcs[a][1]]))
    objective.SetMinimization()

    start_time = time.time()
    solver.Solve()
    temps = time.time() - start_time

    if afficher:
        print('Solution:')
        print('Objective value = {:.1f}'.format(objective.Value()))
        for i in range(k):
            for a in range(m):
                if (X[a][i].solution_value() > 1e-6):
                    print("X_" + str(arcs[a][0]) + "" + str(arcs[a][1]) + "" + str(i + 1) + " = {:.1f}".format(
                        X[a][i].solution_value()))
        print("\nTemps d'execution (s) =", temps)

    return objective.Value(), temps