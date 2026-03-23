"""
Algoritmo A* (A-Star)
"""
import heapq
from maze_solver.utils.constants import DIRS
from .base import SearchAlgorithm


class AStarAlgorithm(SearchAlgorithm):
    """Algoritmo A* (A-Star)"""
    
    name = "A*"
    
    def __init__(self, maze, rows, cols, start, goal, heuristic):
        super().__init__(maze, rows, cols, start, goal)
        self.heuristic = heuristic
    
    def solve(self, callback=None):
        g_cost = {self.start: 0}
        h0 = self.heuristic(self.start, self.goal)
        pq = [(h0, 0, self.start)]
        parent = {self.start: None}
        visited = set()
        self.nodes_explored = 0
        
        while pq:
            f, g, cur = heapq.heappop(pq)
            
            if cur in visited:
                continue
            
            visited.add(cur)
            self.nodes_explored += 1
            
            if cur == self.goal:
                self.visited = visited
                return self.reconstruct_path(parent), self.nodes_explored, visited
            
            for dr, dc in DIRS:
                nr, nc = cur[0] + dr, cur[1] + dc
                nxt = (nr, nc)
                
                if not self.is_valid(nr, nc) or nxt in visited:
                    continue
                
                ng = g + 1
                if ng < g_cost.get(nxt, float('inf')):
                    g_cost[nxt] = ng
                    parent[nxt] = cur
                    heapq.heappush(
                        pq, 
                        (ng + self.heuristic(nxt, self.goal), ng, nxt)
                    )
            
            if callback:
                callback(visited, {item[2] for item in pq})
        
        self.visited = visited
        return None, self.nodes_explored, visited


__all__ = ['AStarAlgorithm']
