import numpy as np
import random
import pandas as pd

# Permet de figer la graine afin d'avoir toujours la même instance
np.random.seed(1)

# création du graphe
def generateGraph(n, m):
    mat = np.zeros(shape=(n, n))
    i = 0
    while i < m:
        u = np.random.randint(0, n)
        v = np.random.randint(0, n)
        if u == v:
            continue;
        if mat[u][v] > 1:
            continue;
        if np.random.randint(0, 2) == 0:
            mat[u][v] = 10
        else:
            mat[u][v] = 20
        i += 1
    # transforme les distances en entier pour les outils google
    mat = mat.astype(int)
    return mat


# création des demandes
def generateDemands(k,n):
    demands = []
    i = 0
    while i < k:
        s = np.random.randint(0, n)
        t = np.random.randint(0, n)
        if s == t:
            continue;
        demands += [[s, t, np.random.randint(1, 5)]]
        i += 1
    # transforme les distances en entier pour les outils google
    return demands


# generate costs de chaque arcs
def generateCosts(M):
    n = len(M)
    mat = np.zeros(shape=(n, n))
    for i in range(n):
        for j in range(n):
            if M[i][j] > 0:
                mat[i][j] = np.random.randint(1, M[i][j])

    mat = mat.astype(int)
    return mat