"""
Funciones heurísticas para algoritmos de búsqueda
"""
import math


def heuristic_manhattan(a, b):
    """Distancia de Manhattan entre dos puntos"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic_euclidean(a, b):
    """Distancia Euclidiana entre dos puntos"""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


__all__ = ['heuristic_manhattan', 'heuristic_euclidean']
