"""
Constantes: colores, configuración y directorios
"""

# ═════════════════════════════════════════════
#  COLORES (RGB)
# ═════════════════════════════════════════════
COLORS = {
    'bg':         '#0D0D0D',
    'wall':       '#1A1A1A',
    'free':       '#0B0B0B',
    'start':      '#C8F050',
    'goal':       '#F05090',
    'visited':    '#0D2030',
    'frontier':   '#143A20',
    'path':       '#50C8F0',
    'ui_bg':      '#161616',
    'ui_border':  '#2A2A2A',
    'text':       '#E8E8E0',
    'muted':      '#6B6B65',
    'accent':     '#C8F050',
    'accent2':    '#50C8F0',
    'accent3':    '#F05090',
    'accent4':    '#F0C050',
}

# ═════════════════════════════════════════════
#  DIRECCIONES (Up, Right, Down, Left)
# ═════════════════════════════════════════════
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# ═════════════════════════════════════════════
#  TIPOS DE CELDA EN LABERINTO
# ═════════════════════════════════════════════
CELL_WALL = 1
CELL_FREE = 0
CELL_START = 2
CELL_GOAL = 3
