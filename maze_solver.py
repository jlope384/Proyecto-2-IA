"""
Maze Solver — Proyecto #2 IA CC3085
Algoritmos: BFS, DFS, Greedy Best-First, A*
Heurísticas: Manhattan, Euclidiana
Uso: python maze_solver.py [archivo.txt]
"""

import pygame
import sys
import time
import math
import heapq
import random
import os
from collections import deque

# ─────────────────────────────────────────
#  COLORES
# ─────────────────────────────────────────
BG         = (13,  13,  13)
WALL       = (26,  26,  26)
FREE       = (11,  11,  11)
START      = (200, 240,  80)
GOAL       = (240,  80, 144)
VISITED    = (13,  32,  48)
FRONTIER   = (20,  58,  32)
PATH       = (80, 200, 240)
UI_BG      = (22,  22,  22)
UI_BORDER  = (42,  42,  42)
TEXT       = (232, 232, 224)
MUTED      = (107, 107, 101)
ACCENT     = (200, 240,  80)
ACCENT2    = ( 80, 200, 240)
ACCENT3    = (240,  80, 144)
ACCENT4    = (240, 192,  80)
BTN_HOVER  = (40,  40,  40)

SIDEBAR_W  = 300
FPS        = 60

# ─────────────────────────────────────────
#  LABERINTO
# ─────────────────────────────────────────
def load_maze(path):
    with open(path) as f:
        lines = [l.rstrip('\n') for l in f if l.strip()]
    rows = len(lines)
    cols = max(len(l) for l in lines)
    maze = []
    start = goal = None
    for r, line in enumerate(lines):
        row = []
        for c in range(cols):
            ch = line[c] if c < len(line) else '1'
            val = int(ch) if ch in '01234' else 1
            row.append(val)
            if ch == '2': start = (r, c)
            if ch == '3': goal  = (r, c)
        maze.append(row)
    return maze, rows, cols, start, goal

def load_maze_from_text(text):
    lines = [l.rstrip('\n') for l in text.strip().split('\n') if l.strip()]
    rows = len(lines)
    cols = max(len(l) for l in lines)
    maze = []
    start = goal = None
    for r, line in enumerate(lines):
        row = []
        for c in range(cols):
            ch = line[c] if c < len(line) else '1'
            val = int(ch) if ch in '01234' else 1
            row.append(val)
            if ch == '2': start = (r, c)
            if ch == '3': goal  = (r, c)
        maze.append(row)
    return maze, rows, cols, start, goal

# ─────────────────────────────────────────
#  ALGORITMOS
# ─────────────────────────────────────────
DIRS = [(-1,0),(0,1),(1,0),(0,-1)]  # Arriba, Derecha, Abajo, Izquierda

def is_valid(maze, rows, cols, r, c):
    return 0 <= r < rows and 0 <= c < cols and maze[r][c] != 1

def reconstruct(parent, goal):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

def heuristic_manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def heuristic_euclidean(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def bfs(maze, rows, cols, start, goal, callback=None):
    queue   = deque([start])
    parent  = {start: None}
    visited = set([start])
    nodes   = 0
    while queue:
        cur = queue.popleft()
        nodes += 1
        if cur == goal:
            return reconstruct(parent, goal), nodes, visited
        for dr, dc in DIRS:
            nr, nc = cur[0]+dr, cur[1]+dc
            nxt = (nr, nc)
            if is_valid(maze, rows, cols, nr, nc) and nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                queue.append(nxt)
        if callback: callback(visited, set(queue))
    return None, nodes, visited

def dfs(maze, rows, cols, start, goal, callback=None):
    stack   = [start]
    parent  = {start: None}
    visited = set([start])
    nodes   = 0
    while stack:
        cur = stack.pop()
        nodes += 1
        if cur == goal:
            return reconstruct(parent, goal), nodes, visited
        for dr, dc in DIRS:
            nr, nc = cur[0]+dr, cur[1]+dc
            nxt = (nr, nc)
            if is_valid(maze, rows, cols, nr, nc) and nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                stack.append(nxt)
        if callback: callback(visited, set(stack))
    return None, nodes, visited

def greedy(maze, rows, cols, start, goal, hfunc, callback=None):
    h0  = hfunc(start, goal)
    pq  = [(h0, start)]
    parent  = {start: None}
    visited = set([start])
    nodes   = 0
    while pq:
        _, cur = heapq.heappop(pq)
        nodes += 1
        if cur == goal:
            return reconstruct(parent, goal), nodes, visited
        for dr, dc in DIRS:
            nr, nc = cur[0]+dr, cur[1]+dc
            nxt = (nr, nc)
            if is_valid(maze, rows, cols, nr, nc) and nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                heapq.heappush(pq, (hfunc(nxt, goal), nxt))
        if callback: callback(visited, {item[1] for item in pq})
    return None, nodes, visited

def astar(maze, rows, cols, start, goal, hfunc, callback=None):
    g_cost  = {start: 0}
    h0      = hfunc(start, goal)
    pq      = [(h0, 0, start)]
    parent  = {start: None}
    visited = set()
    nodes   = 0
    while pq:
        f, g, cur = heapq.heappop(pq)
        if cur in visited: continue
        visited.add(cur)
        nodes += 1
        if cur == goal:
            return reconstruct(parent, goal), nodes, visited
        for dr, dc in DIRS:
            nr, nc = cur[0]+dr, cur[1]+dc
            nxt = (nr, nc)
            if not is_valid(maze, rows, cols, nr, nc) or nxt in visited: continue
            ng = g + 1
            if ng < g_cost.get(nxt, float('inf')):
                g_cost[nxt] = ng
                parent[nxt] = cur
                heapq.heappush(pq, (ng + hfunc(nxt, goal), ng, nxt))
        if callback: callback(visited, {item[2] for item in pq})
    return None, nodes, visited

# ─────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────
class Button:
    def __init__(self, rect, label, color=None, text_color=None, small=False):
        self.rect       = pygame.Rect(rect)
        self.label      = label
        self.color      = color or UI_BORDER
        self.text_color = text_color or TEXT
        self.small      = small
        self.hovered    = False
        self.active     = False
        self.enabled    = True

    def draw(self, surf, font):
        bg = (40, 40, 40) if self.hovered and self.enabled else UI_BG
        if self.active:
            bg = self.text_color
        pygame.draw.rect(surf, bg, self.rect, border_radius=4)
        pygame.draw.rect(surf, self.color if self.enabled else (40,40,40),
                         self.rect, 1, border_radius=4)
        col = (0,0,0) if self.active else (self.text_color if self.enabled else MUTED)
        txt = font.render(self.label, True, col)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos) and self.enabled

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and self.enabled

class MetricCard:
    def __init__(self, rect, label, color):
        self.rect  = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.value = '—'

    def draw(self, surf, font_sm, font_lg):
        pygame.draw.rect(surf, (30,30,30), self.rect, border_radius=4)
        pygame.draw.rect(surf, UI_BORDER, self.rect, 1, border_radius=4)
        lbl = font_sm.render(self.label, True, MUTED)
        surf.blit(lbl, (self.rect.x+10, self.rect.y+8))
        val = font_lg.render(str(self.value), True, self.color)
        surf.blit(val, (self.rect.x+10, self.rect.y+24))

# ─────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────
class MazeSolverApp:
    def __init__(self, maze_file=None):
        pygame.init()
        self.W, self.H = 1280, 800
        self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
        pygame.display.set_caption("Maze Solver — Proyecto #2 IA CC3085")
        self.clock = pygame.time.Clock()

        self.font_sm  = pygame.font.SysFont('Courier New', 11)
        self.font_md  = pygame.font.SysFont('Courier New', 13, bold=True)
        self.font_lg  = pygame.font.SysFont('Courier New', 20, bold=True)
        self.font_xl  = pygame.font.SysFont('Courier New', 14, bold=True)

        # State
        self.maze         = None
        self.rows         = 0
        self.cols         = 0
        self.start        = None
        self.goal         = None
        self.orig_start   = None
        self.cell         = 10
        self.visited      = set()
        self.frontier     = set()
        self.path         = []
        self.running_algo = False
        self.status       = "Cargue un laberinto con la tecla [O] o arrastre un .txt"
        self.status_color = MUTED
        self.algo         = 'BFS'
        self.heuristic    = 'manhattan'
        self.anim_speed   = 30   # frames entre updates de visualización
        self.compare_results = []

        self._build_ui()

        if maze_file and os.path.exists(maze_file):
            self._load_file(maze_file)

    def _build_ui(self):
        x = 10
        y = 10
        w = SIDEBAR_W - 20

        # Algo buttons
        self.btn_bfs    = Button((x,   y+30, w//2-3, 30), 'BFS',    ACCENT,  ACCENT)
        self.btn_dfs    = Button((x+w//2+3, y+30, w//2-3, 30), 'DFS',    ACCENT,  ACCENT)
        self.btn_greedy = Button((x,   y+65, w//2-3, 30), 'Greedy', ACCENT,  ACCENT)
        self.btn_astar  = Button((x+w//2+3, y+65, w//2-3, 30), 'A*',     ACCENT,  ACCENT)
        self.algo_buttons = [self.btn_bfs, self.btn_dfs, self.btn_greedy, self.btn_astar]
        self.btn_bfs.active = True

        self.btn_manh   = Button((x,     y+118, w//2-3, 26), 'Manhattan', ACCENT2, ACCENT2, small=True)
        self.btn_eucl   = Button((x+w//2+3, y+118, w//2-3, 26), 'Euclidiana', ACCENT2, ACCENT2, small=True)
        self.heur_buttons = [self.btn_manh, self.btn_eucl]
        self.btn_manh.active = True

        self.btn_run    = Button((x, y+162, w, 34), '▶  EJECUTAR',  ACCENT,  (0,0,0))
        self.btn_run.color = ACCENT; self.btn_run.text_color = (0,0,0)
        self.btn_all    = Button((x, y+200, w, 28), '◈  COMPARAR TODOS', ACCENT2, (0,0,0))
        self.btn_all.color = ACCENT2; self.btn_all.text_color = (0,0,0)
        self.btn_clear  = Button((x, y+232, w//2-3, 26), '✕ Limpiar',  UI_BORDER, MUTED, small=True)
        self.btn_random = Button((x+w//2+3, y+232, w//2-3, 26), '⊕ Aleatorio', ACCENT2, ACCENT2, small=True)
        self.btn_open   = Button((x, y+262, w, 26), '[O] Cargar laberinto .txt', UI_BORDER, MUTED, small=True)

        # Speed slider area (manual)
        self.speed_rect = pygame.Rect(x, y+302, w, 14)
        self.speed_val  = 2   # 0=fast .. 4=slow

        # Metrics
        my = y+340
        mh = 52
        mg = 6
        self.card_path  = MetricCard((x, my,          w, mh), 'LARGO DEL CAMINO', ACCENT)
        self.card_nodes = MetricCard((x, my+mh+mg,     w, mh), 'NODOS EXPLORADOS',  ACCENT2)
        self.card_time  = MetricCard((x, my+2*(mh+mg), w, mh), 'TIEMPO (ms)',       ACCENT3)

        self.all_buttons = [
            self.btn_bfs, self.btn_dfs, self.btn_greedy, self.btn_astar,
            self.btn_manh, self.btn_eucl,
            self.btn_run, self.btn_all, self.btn_clear, self.btn_random, self.btn_open
        ]

    def _load_file(self, path):
        try:
            self.maze, self.rows, self.cols, self.start, self.goal = load_maze(path)
            if not self.start: raise ValueError("No se encontró punto de inicio '2'")
            if not self.goal:  raise ValueError("No se encontró punto de salida '3'")
            self.orig_start = self.start
            self._fit_cell()
            self._reset_state()
            self.status = f"Laberinto {self.rows}×{self.cols} | inicio {self.start} → meta {self.goal}"
            self.status_color = ACCENT2
            self.compare_results = []
        except Exception as e:
            self.status = f"Error: {e}"
            self.status_color = ACCENT3

    def _fit_cell(self):
        area_w = self.W - SIDEBAR_W - 20
        area_h = self.H - 20
        self.cell = max(4, min(14, min(area_w // self.cols, area_h // self.rows)))

    def _reset_state(self):
        self.visited  = set()
        self.frontier = set()
        self.path     = []
        self.card_path.value  = '—'
        self.card_nodes.value = '—'
        self.card_time.value  = '—'

    # ─── DRAWING ───────────────────────────────
    def _draw_maze(self):
        if not self.maze: return
        ox = SIDEBAR_W + 10
        oy = 10
        c  = self.cell
        surf = self.screen
        for r in range(self.rows):
            for col in range(self.cols):
                pos = (r, col)
                v = self.maze[r][col]
                if v == 1:
                    color = WALL
                elif pos == self.start:
                    color = START
                elif pos == self.goal:
                    color = GOAL
                elif pos in self.path:
                    color = PATH
                elif pos in self.frontier:
                    color = FRONTIER
                elif pos in self.visited:
                    color = VISITED
                else:
                    color = FREE
                pygame.draw.rect(surf, color, (ox + col*c, oy + r*c, c, c))

    def _draw_sidebar(self):
        pygame.draw.rect(self.screen, UI_BG, (0, 0, SIDEBAR_W, self.H))
        pygame.draw.line(self.screen, UI_BORDER, (SIDEBAR_W, 0), (SIDEBAR_W, self.H))

        x, w = 10, SIDEBAR_W - 20

        # Title
        t = self.font_xl.render("MAZE SOLVER", True, ACCENT)
        self.screen.blit(t, (x, 10))
        t2 = self.font_sm.render("Proyecto #2 — IA CC3085", True, MUTED)
        self.screen.blit(t2, (x, 28))

        pygame.draw.line(self.screen, UI_BORDER, (x, 46), (x+w, 46))

        # Section labels
        def label(txt, y):
            t = self.font_sm.render(txt, True, MUTED)
            self.screen.blit(t, (x, y))

        label("ALGORITMO", 58)
        label("HEURÍSTICA (Greedy / A*)", 110)
        label("ACCIONES", 156)

        # Speed slider
        label("VELOCIDAD DE ANIMACIÓN", 296)
        speeds = ["Máx", "Rápido", "Normal", "Lento", "Muy lento"]
        sy = 314
        track = pygame.Rect(x, sy+3, w, 8)
        pygame.draw.rect(self.screen, UI_BORDER, track, border_radius=4)
        filled_w = int((self.speed_val / 4) * w)
        pygame.draw.rect(self.screen, ACCENT2, (x, sy+3, filled_w, 8), border_radius=4)
        thumb_x = x + filled_w
        pygame.draw.circle(self.screen, ACCENT2, (thumb_x, sy+7), 8)
        sv_txt = self.font_sm.render(speeds[self.speed_val], True, ACCENT2)
        self.screen.blit(sv_txt, (x+w-sv_txt.get_width(), sy-11))

        # Draw all buttons
        for btn in self.all_buttons:
            btn.draw(self.screen, self.font_md)

        # Metrics
        self.card_path.draw(self.screen, self.font_sm, self.font_lg)
        self.card_nodes.draw(self.screen, self.font_sm, self.font_lg)
        self.card_time.draw(self.screen, self.font_sm, self.font_lg)

        # Status
        st = self.font_sm.render(self.status[:52], True, self.status_color)
        self.screen.blit(st, (x, self.H - 50))
        if len(self.status) > 52:
            st2 = self.font_sm.render(self.status[52:104], True, self.status_color)
            self.screen.blit(st2, (x, self.H - 36))

        # Compare results table
        if self.compare_results:
            ty = self.card_time.rect.bottom + 12
            lbl = self.font_sm.render("COMPARACIÓN", True, MUTED)
            self.screen.blit(lbl, (x, ty)); ty += 16
            headers = ["ALGO", "CAMINO", "NODOS", "ms"]
            col_w = [w//4]*4
            for i, h in enumerate(headers):
                ht = self.font_sm.render(h, True, MUTED)
                self.screen.blit(ht, (x + sum(col_w[:i]), ty))
            ty += 14
            pygame.draw.line(self.screen, UI_BORDER, (x, ty), (x+w, ty)); ty += 4

            # find bests
            valid = [r for r in self.compare_results if r['path'] != 'N/A']
            best_path  = min(r['path']  for r in valid) if valid else None
            best_nodes = min(r['nodes'] for r in valid) if valid else None
            best_time  = min(r['time']  for r in valid) if valid else None

            for row in self.compare_results:
                vals = [row['algo'], str(row['path']), str(row['nodes']), f"{row['time']:.1f}"]
                for i, v in enumerate(vals):
                    is_best = (i==1 and row['path']==best_path) or \
                              (i==2 and row['nodes']==best_nodes) or \
                              (i==3 and abs(row['time']-best_time)<0.01 if best_time else False)
                    col = ACCENT if is_best else TEXT
                    t = self.font_sm.render(v, True, col)
                    self.screen.blit(t, (x + sum(col_w[:i]), ty))
                ty += 14

        # Legend
        legend = [("Pared", WALL), ("Libre", FREE), ("Inicio", START),
                  ("Meta", GOAL), ("Visitado", VISITED), ("Camino", PATH)]
        lx, ly = SIDEBAR_W + 15, self.H - 22
        for name, col in legend:
            pygame.draw.rect(self.screen, col, (lx, ly, 10, 10), border_radius=2)
            pygame.draw.rect(self.screen, UI_BORDER, (lx, ly, 10, 10), 1, border_radius=2)
            t = self.font_sm.render(name, True, MUTED)
            self.screen.blit(t, (lx+13, ly))
            lx += t.get_width() + 28

    # ─── ANIMATION CALLBACK ─────────────────
    def _make_callback(self):
        delay_map = [0, 5, 15, 30, 60]
        delay_ms  = delay_map[self.speed_val]
        frame_step = max(1, 20 - self.speed_val * 4)
        counter = [0]

        def cb(visited, frontier):
            counter[0] += 1
            if counter[0] % frame_step != 0:
                return
            self.visited  = visited
            self.frontier = frontier
            self.screen.fill(BG)
            self._draw_maze()
            self._draw_sidebar()
            pygame.display.flip()
            if delay_ms: pygame.time.wait(delay_ms)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
        return cb

    # ─── RUN ALGORITHM ──────────────────────
    def _get_hfunc(self):
        if self.heuristic == 'euclidean':
            return heuristic_euclidean
        return heuristic_manhattan

    def _run_algo(self, algo_name, for_compare=False):
        if not self.maze or self.running_algo: return None
        self.running_algo = True
        if not for_compare:
            self._reset_state()
        self.status = f"Ejecutando {algo_name}..."
        self.status_color = ACCENT

        cb    = self._make_callback()
        hfunc = self._get_hfunc()
        t0    = time.perf_counter()

        if algo_name == 'BFS':
            path, nodes, visited = bfs(self.maze, self.rows, self.cols, self.start, self.goal, cb)
        elif algo_name == 'DFS':
            path, nodes, visited = dfs(self.maze, self.rows, self.cols, self.start, self.goal, cb)
        elif algo_name == 'Greedy':
            path, nodes, visited = greedy(self.maze, self.rows, self.cols, self.start, self.goal, hfunc, cb)
        else:  # A*
            path, nodes, visited = astar(self.maze, self.rows, self.cols, self.start, self.goal, hfunc, cb)

        elapsed = (time.perf_counter() - t0) * 1000

        self.visited  = visited
        self.frontier = set()
        self.path     = set(path) if path else set()

        if path:
            self.card_path.value  = len(path)
            self.card_nodes.value = nodes
            self.card_time.value  = f"{elapsed:.2f}"
            self.status = f"{algo_name} OK | camino={len(path)} nodos={nodes} t={elapsed:.1f}ms"
            self.status_color = ACCENT2
        else:
            self.card_path.value  = 'N/A'
            self.card_nodes.value = nodes
            self.card_time.value  = f"{elapsed:.2f}"
            self.status = f"{algo_name}: No se encontró solución."
            self.status_color = ACCENT3

        self.running_algo = False
        return {'algo': algo_name, 'path': len(path) if path else 'N/A',
                'nodes': nodes, 'time': elapsed}

    def _run_all(self):
        if not self.maze or self.running_algo: return
        self.compare_results = []
        algos = ['BFS', 'DFS', 'Greedy', 'A*']
        for algo in algos:
            self._reset_state()
            res = self._run_algo(algo, for_compare=True)
            if res: self.compare_results.append(res)
            pygame.time.wait(200)

    # ─── EVENTS ────────────────────────────
    def _handle_speed_click(self, pos):
        if not self.speed_rect.inflate(0, 20).collidepoint(pos): return False
        rx = pos[0] - self.speed_rect.x
        self.speed_val = max(0, min(4, int(rx / self.speed_rect.width * 4 + 0.5)))
        return True

    def _open_file_dialog(self):
        # Pygame doesn't have a native dialog; use stdin hint
        self.status = "Arrastra un .txt a la ventana o pasa la ruta como argumento."
        self.status_color = MUTED

    def _handle_drop(self, path):
        if path.endswith('.txt'):
            self._load_file(path)

    def run(self):
        while True:
            self.W, self.H = self.screen.get_size()
            if self.maze: self._fit_cell()
            self._rebuild_ui_positions()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.DROPFILE:
                    self._handle_drop(event.file)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        self._open_file_dialog()
                    if event.key == pygame.K_r and self.maze:
                        self._run_algo(self.algo)
                    if event.key == pygame.K_c and self.maze:
                        self.start = self.orig_start
                        self._reset_state()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    for btn in self.all_buttons:
                        btn.check_hover(event.pos)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos

                    if self._handle_speed_click(pos): continue

                    # Algo selection
                    for btn, name in zip(self.algo_buttons, ['BFS','DFS','Greedy','A*']):
                        if btn.is_clicked(pos):
                            for b in self.algo_buttons: b.active = False
                            btn.active = True
                            self.algo = name

                    # Heuristic selection
                    for btn, name in zip(self.heur_buttons, ['manhattan','euclidean']):
                        if btn.is_clicked(pos):
                            for b in self.heur_buttons: b.active = False
                            btn.active = True
                            self.heuristic = name

                    if self.btn_run.is_clicked(pos)    and self.maze: self._run_algo(self.algo)
                    if self.btn_all.is_clicked(pos)    and self.maze: self._run_all()
                    if self.btn_open.is_clicked(pos):                  self._open_file_dialog()
                    if self.btn_clear.is_clicked(pos)  and self.maze:
                        self.start = self.orig_start
                        self._reset_state()
                        self.compare_results = []
                        self.status = "Laberinto limpiado."
                        self.status_color = MUTED
                    if self.btn_random.is_clicked(pos) and self.maze:
                        free = [(r, c) for r in range(self.rows)
                                for c in range(self.cols)
                                if self.maze[r][c] in (0, 2)]
                        if free:
                            self.start = random.choice(free)
                            self._reset_state()
                            self.status = f"Inicio aleatorio: {self.start}"
                            self.status_color = ACCENT2

            self.screen.fill(BG)
            self._draw_maze()
            self._draw_sidebar()
            pygame.display.flip()
            self.clock.tick(FPS)

    def _rebuild_ui_positions(self):
        """Rebuild button rects based on current window size."""
        x  = 10
        w  = SIDEBAR_W - 20
        y0 = 58

        half = w//2 - 3
        gap  = 6

        self.btn_bfs.rect    = pygame.Rect(x,          y0+12, half, 30)
        self.btn_dfs.rect    = pygame.Rect(x+half+gap, y0+12, half, 30)
        self.btn_greedy.rect = pygame.Rect(x,          y0+46, half, 30)
        self.btn_astar.rect  = pygame.Rect(x+half+gap, y0+46, half, 30)

        self.btn_manh.rect   = pygame.Rect(x,          y0+96, half, 26)
        self.btn_eucl.rect   = pygame.Rect(x+half+gap, y0+96, half, 26)

        self.btn_run.rect    = pygame.Rect(x, y0+140, w, 34)
        self.btn_all.rect    = pygame.Rect(x, y0+178, w, 28)
        self.btn_clear.rect  = pygame.Rect(x,          y0+210, half, 26)
        self.btn_random.rect = pygame.Rect(x+half+gap, y0+210, half, 26)
        self.btn_open.rect   = pygame.Rect(x, y0+240, w, 26)

        self.speed_rect      = pygame.Rect(x, y0+290, w, 14)

        my = y0 + 320
        mh, mg = 52, 6
        self.card_path.rect  = pygame.Rect(x, my,          w, mh)
        self.card_nodes.rect = pygame.Rect(x, my+mh+mg,    w, mh)
        self.card_time.rect  = pygame.Rect(x, my+2*(mh+mg),w, mh)

        self.all_buttons = [
            self.btn_bfs, self.btn_dfs, self.btn_greedy, self.btn_astar,
            self.btn_manh, self.btn_eucl,
            self.btn_run, self.btn_all, self.btn_clear, self.btn_random, self.btn_open
        ]


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────
if __name__ == '__main__':
    maze_file = sys.argv[1] if len(sys.argv) > 1 else None
    app = MazeSolverApp(maze_file)
    app.run()
