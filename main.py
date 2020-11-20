from __future__ import print_function
from ortools.graph import pywrapgraph



def main():
    arc_depart = [0, 0, 1, 1, 1, 2, 2, 3, 4]
    arc_arrivee = [1, 2, 2, 3, 4, 3, 4, 4, 2]
    cout = [4, 4, 2, 2, 6, 1, 3, 2, 3]
    capa = [15, 8, 20, 4, 10, 15, 4, 20, 5]

    offre = [20, 0, 0, -5, -15]


