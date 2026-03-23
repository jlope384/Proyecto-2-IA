"""
Clase base para algoritmos de búsqueda
"""


class SearchAlgorithm:
    """Clase base para todos los algoritmos de búsqueda"""
    
    name = "Base Algorithm"
    
    def __init__(self, maze, rows, cols, start, goal):
        self.maze = maze
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.visited = set()
        self.nodes_explored = 0
    
    def is_valid(self, r, c):
        """Verifica si una celda es válida (dentro de limites y no pared)"""
        return (0 <= r < self.rows and 
                0 <= c < self.cols and 
                self.maze[r][c] != 1)
    
    def reconstruct_path(self, parent):
        """Reconstruye el camino desde inicio hasta meta"""
        path = []
        cur = self.goal
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        path.reverse()
        return path
    
    def solve(self, callback=None):
        """Ejecuta el algoritmo. Debe ser implementado por subclases"""
        raise NotImplementedError("Subclasses must implement solve()")


__all__ = ['SearchAlgorithm']
