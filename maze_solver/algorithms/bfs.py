"""
Algoritmo BFS (Breadth-First Search)
"""
from collections import deque
from maze_solver.utils.constants import DIRS
from .base import SearchAlgorithm


class BFSAlgorithm(SearchAlgorithm):
    """Búsqueda por amplitud (BFS)"""
    
    name = "BFS"
    
    def solve(self, callback=None):
        queue = deque([self.start])
        parent = {self.start: None}
        visited = set([self.start])
        self.nodes_explored = 0
        
        while queue:
            cur = queue.popleft()
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
                    queue.append(nxt)
            
            if callback:
                callback(visited, set(queue))
        
        self.visited = visited
        return None, self.nodes_explored, visited


__all__ = ['BFSAlgorithm']
