"""
Funciones para cargar y procesar laberintos
"""


def load_maze(path):
    """Carga un laberinto desde archivo .txt"""
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
            if ch == '2':
                start = (r, c)
            if ch == '3':
                goal = (r, c)
        maze.append(row)
    
    return maze, rows, cols, start, goal


def load_maze_from_text(text):
    """Carga un laberinto desde texto"""
    lines = [l.rstrip('\n') for l in text.strip().split('\n') if l.strip()]
    
    rows = len(lines)
    cols = max(len(l) for l in lines) if lines else 0
    maze = []
    start = goal = None
    
    for r, line in enumerate(lines):
        row = []
        for c in range(cols):
            ch = line[c] if c < len(line) else '1'
            val = int(ch) if ch in '01234' else 1
            row.append(val)
            if ch == '2':
                start = (r, c)
            if ch == '3':
                goal = (r, c)
        maze.append(row)
    
    return maze, rows, cols, start, goal


__all__ = ['load_maze', 'load_maze_from_text']
