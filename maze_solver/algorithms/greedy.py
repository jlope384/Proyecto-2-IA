"""
Algoritmo Greedy Best-First (Greedy)
"""
import heapq
from maze_solver.utils.constants import DIRS
from .base import SearchAlgorithm


class GreedyAlgorithm(SearchAlgorithm):
    """Búsqueda Greedy (Best-First)"""
    
    name = "Greedy"
    
    def __init__(self, maze, rows, cols, start, goal, heuristic):
        super().__init__(maze, rows, cols, start, goal)
        self.heuristic = heuristic
    
    def solve(self, callback=None):
        h0 = self.heuristic(self.start, self.goal)
        pq = [(h0, 0, self.start)]  # (h_value, counter, position)
        counter = 0
        parent = {self.start: None}
        visited = {self.start}  # Marca start como visitado
        self.nodes_explored = 0
        
        while pq:
            _, _, cur = heapq.heappop(pq)
            self.nodes_explored += 1
            
            if cur == self.goal:
                self.visited = visited
                return self.reconstruct_path(parent), self.nodes_explored, visited
            
            for dr, dc in DIRS:
                nr, nc = cur[0] + dr, cur[1] + dc
                nxt = (nr, nc)
                
                if self.is_valid(nr, nc) and nxt not in visited:
                    visited.add(nxt)  # Marca como visitado AL AGREGAR
                    parent[nxt] = cur
                    counter += 1
                    heapq.heappush(pq, (self.heuristic(nxt, self.goal), counter, nxt))
            
            if callback:
                callback(visited, {item[2] for item in pq})
        
        self.visited = visited
        return None, self.nodes_explored, visited


__all__ = ['GreedyAlgorithm']
