# 🧭 Maze Solver — Proyecto #2 IA CC3085

## 📋 Descripción

Aplicación web interactiva para resolver laberintos usando algoritmos de búsqueda. Implementa:

- **Algoritmos**: BFS, DFS, Greedy Best-First, A*
- **Heurísticas**: Manhattan, Euclidiana
- **Comparación**: Ejecuta todos los algoritmos y compara resultados
- **Visualización**: Interfaz web moderna con Streamlit

## 📁 Estructura del Proyecto

```
.
├── app.py                       # Aplicación principal (Streamlit)
├── requirements.txt             # Dependencias Python
├── README.md                    # Este archivo
└── maze_solver/                 # Módulo principal
    ├── __init__.py
    ├── algorithms/              # Algoritmos de búsqueda
    │   ├── __init__.py
    │   ├── base.py              # Clase base SearchAlgorithm
    │   ├── bfs.py               # Búsqueda por amplitud
    │   ├── dfs.py               # Búsqueda por profundidad
    │   ├── greedy.py            # Greedy Best-First
    │   └── astar.py             # Algoritmo A*
    ├── utils/                   # Funciones auxiliares
    │   ├── __init__.py
    │   ├── constants.py         # Colores y constantes
    │   ├── heuristics.py        # Funciones heurísticas
    │   └── maze.py              # Carga y procesamiento
    └── ui/                      # Componentes de interfaz
        ├── __init__.py
        └── components.py        # Visualización con Plotly
```

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd Proyecto-2-IA
```

### 2. Crear entorno virtual (recomendado)

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### Cargar un laberinto

1. **Opción A:** Subir un archivo `.txt` con el formato:
   ```
   1 1 1 1 1
   2 0 0 0 3
   1 1 1 1 1
   ```
   Donde:
   - `1` = Pared
   - `0` = Espacio libre
   - `2` = Punto de inicio
   - `3` = Punto de meta

2. **Opción B:** Generar un laberinto aleatorio con el botón "🎲 Generar"

### Ejecutar algoritmos

1. Selecciona un algoritmo (BFS, DFS, Greedy, A*)
2. Selecciona una heurística (solo para Greedy y A*)
3. Haz clic en "▶ Ejecutar"

### Comparar todos los algoritmos

Haz clic en "◈ Comparar todos" para ejecutar todos los algoritmos simultáneamente

## 📊 Módulos

### `maze_solver.algorithms`

Implementación de algoritmos de búsqueda:

- **BFSAlgorithm**: Breadth-First Search
- **DFSAlgorithm**: Depth-First Search
- **GreedyAlgorithm**: Greedy Best-First Search
- **AStarAlgorithm**: A* Search

Todos heredan de `SearchAlgorithm` (clase base)

```python
from maze_solver.algorithms import BFSAlgorithm

algo = BFSAlgorithm(maze, rows, cols, start, goal)
path, nodes, visited = algo.solve()
```

### `maze_solver.utils`

Funciones auxiliares:

- **load_maze(path)**: Carga laberinto desde archivo
- **load_maze_from_text(text)**: Carga laberinto desde string
- **heuristic_manhattan(a, b)**: Distancia Manhattan
- **heuristic_euclidean(a, b)**: Distancia Euclidiana

### `maze_solver.ui`

Componentes de visualización:

- **draw_maze_plotly()**: Dibuja el laberinto con Plotly
- **metric_card()**: Tarjeta de métrica
- **comparison_table()**: Tabla de comparación

## 🎨 Colores

| Color | RGB | Uso |
|-------|-----|-----|
| Pared | (26,26,26) | Obstáculos |
| Libre | (17,17,17) | Espacio transitable |
| Inicio | (200,240,80) | Punto de inicio |
| Meta | (240,80,144) | Punto de llegada |
| Visitado | (32,64,96) | Celdas exploradas |
| Frontera | (32,128,64) | Nodos en cola/pila |
| Camino | (80,200,240) | Ruta solución |

## 📈 Métricas

Cada algoritmo reporta:

- **Largo del camino**: Número de pasos en la solución
- **Nodos explorados**: Cantidad de celdas procesadas
- **Tiempo**: Tiempo de ejecución en milisegundos

## 🔧 Ejemplos de uso

### Crear un algoritmo personalizado

```python
from maze_solver.algorithms.base import SearchAlgorithm

class MyAlgorithm(SearchAlgorithm):
    name = "Mi Algoritmo"
    
    def solve(self, callback=None):
        # Tu implementación aquí
        return path, nodes_explored, visited
```

### Usar los algoritmos directamente

```python
from maze_solver.utils import load_maze, heuristic_manhattan
from maze_solver.algorithms import AStarAlgorithm

maze, rows, cols, start, goal = load_maze('laberinto.txt')

algo = AStarAlgorithm(maze, rows, cols, start, goal, heuristic_manhattan)
path, nodes, visited = algo.solve()

print(f"Camino encontrado: {len(path)} pasos")
print(f"Nodos explorados: {nodes}")
```

## 📚 Formato de archivo de laberinto

El archivo debe ser un `.txt` con una matriz de números:

```
1 1 1 1 1 1 1 1 1 1
1 2 0 0 0 1 0 0 0 1
1 0 1 1 0 1 0 1 0 1
1 0 0 0 0 0 0 1 0 1
1 0 1 1 1 1 1 1 0 1
1 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 3 1
1 1 1 1 1 1 1 1 1 1
```

## 🎓 Conceptos Educativos

### Algoritmos implementados

- **BFS**: Exploración por niveles, encuentra camino más corto en grafos no ponderados
- **DFS**: Exploración en profundidad, usa menos memoria pero puede no encontrar camino óptimo
- **Greedy**: Selecciona el nodo más prometedor según heurística, rápido pero no garantiza óptimo
- **A***: Combina costo real (g) y heurístico (h), optimalidad garantizada con heurística admisible

### Heurísticas

- **Manhattan**: |x1-x2| + |y1-y2| (movimientos ortogonales)
- **Euclidiana**: √((x1-x2)² + (y1-y2)²) (línea recta)

## 🐛 Solución de problemas

### "ModuleNotFoundError: No module named 'maze_solver'"

Asegúrate de estar en el directorio raíz del proyecto y que `PYTHONPATH` incluya el directorio actual:

```bash
# Windows
set PYTHONPATH=%PYTHONPATH%;.

# macOS/Linux
export PYTHONPATH=$PYTHONPATH:.
```

### La app no se abre en el navegador

Streamlit automaticamente abrirá la ventana, pero si no lo hace, visita:
```
http://localhost:8501
```

## 📝 Requisitos

- Python 3.8+
- Las dependencias listadas en `requirements.txt`

## 👨‍💻 Autor

**Proyecto Final**
- Universidad del Valle de Guatemala
- Curso: Inteligencia Artificial (CC3085)
- Proyecto #2: Maze Solver

## 📄 Licencia

MIT
