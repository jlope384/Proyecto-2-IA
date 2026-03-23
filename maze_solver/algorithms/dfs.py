"""
Algoritmo DFS (Depth-First Search)
"""
from maze_solver.utils.constants import DIRS
from .base import SearchAlgorithm


class DFSAlgorithm(SearchAlgorithm):
    """Búsqueda por profundidad (DFS)"""
    
    name = "DFS"
    
    def solve(self, callback=None):
        stack = [self.start]
        parent = {self.start: None}
        visited = set([self.start])
        self.nodes_explored = 0
        
        while stack:
            cur = stack.pop()
            self.nodes_explored += 1
            
            if cur == self.goal:
                self.visited = visited
                return self.reconstruct_path(parent), self.nodes_explored, visited
            
            for dr, dc in DIRS:
                nr, nc = cur[0] + dr, cur[1] + dc
                nxt = (nr, nc)
                
                if self.is_valid(nr, nc) and nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = cur
                    stack.append(nxt)
            
            if callback:
                callback(visited, set(stack))
        
        self.visited = visited
        return None, self.nodes_explored, visited


__all__ = ['DFSAlgorithm']
