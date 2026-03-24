"""
Maze Solver — Proyecto #2 IA CC3085
Aplicacion web con Streamlit

Algoritmos: BFS, DFS, Greedy Best-First, A*
Heuristicas: Manhattan, Euclidiana
"""

import streamlit as st
import time
import random
import pandas as pd
from io import StringIO

from maze_solver.utils import (
    load_maze,
    load_maze_from_text,
    heuristic_manhattan,
    heuristic_euclidean,
)
from maze_solver.algorithms import (
    BFSAlgorithm,
    DFSAlgorithm,
    GreedyAlgorithm,
    AStarAlgorithm,
)
from maze_solver.ui.components import (
    draw_maze_plotly,
    metric_card,
)


# ═════════════════════════════════════════════════════════════════
#  CONFIGURACIÓN DE LA PÁGINA
# ═════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Maze Solver | IA CC3085",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado
st.markdown("""
<style>
    :root {
        --primary: #C8F050;
        --secondary: #50C8F0;
        --accent: #F05090;
        --dark: #0D0D0D;
        --darker: #161616;
    }
    
    body {
        background: var(--dark);
        color: #E8E8E0;
    }
    
    .stApp {
        background: var(--dark);
    }
    
    .main {
        background: var(--dark);
    }
    
    .stSidebar {
        background: var(--darker);
    }
    
    h1, h2, h3 {
        color: var(--primary);
    }
    
    .metric-card {
        background: var(--darker);
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════
#  STATE MANAGEMENT
# ═════════════════════════════════════════════════════════════════
def init_session_state():
    """Inicializa el estado de la sesion"""
    if 'maze' not in st.session_state:
        st.session_state.maze = None
        st.session_state.rows = 0
        st.session_state.cols = 0
        st.session_state.start = None
        st.session_state.goal = None
        st.session_state.orig_start = None
        st.session_state.visited = set()
        st.session_state.frontier = set()
        st.session_state.path = []
        st.session_state.algorithm = "BFS"
        st.session_state.heuristic = "manhattan"
        st.session_state.results = []
        st.session_state.compare_results = []
        st.session_state.last_result = None


def reset_maze_state():
    """Resetea el estado del laberinto"""
    st.session_state.visited = set()
    st.session_state.frontier = set()
    st.session_state.path = []
    st.session_state.last_result = None


def load_maze_data(maze, rows, cols, start, goal):
    """Carga datos del laberinto en el estado"""
    st.session_state.maze = maze
    st.session_state.rows = rows
    st.session_state.cols = cols
    st.session_state.start = start
    st.session_state.goal = goal
    st.session_state.orig_start = start
    reset_maze_state()


# ═════════════════════════════════════════════════════════════════
#  ALGORITMOS
# ═════════════════════════════════════════════════════════════════
def run_algorithm(algo_name):
    """
    Ejecuta un algoritmo de búsqueda
    
    Args:
        algo_name: Nombre del algoritmo (BFS, DFS, Greedy, A*)
    
    Returns:
        dict con resultados (path, nodes, time)
    """
    if not st.session_state.maze:
        return None
    
    # Seleccionar algoritmo
    hfunc = heuristic_euclidean if st.session_state.heuristic == "euclidean" else heuristic_manhattan
    
    algo_class = {
        'BFS': BFSAlgorithm,
        'DFS': DFSAlgorithm,
        'Greedy': GreedyAlgorithm,
        'A*': AStarAlgorithm,
    }[algo_name]
    
    # Crear instancia del algoritmo
    if algo_name in ['Greedy', 'A*']:
        algo = algo_class(
            st.session_state.maze,
            st.session_state.rows,
            st.session_state.cols,
            st.session_state.start,
            st.session_state.goal,
            hfunc
        )
    else:
        algo = algo_class(
            st.session_state.maze,
            st.session_state.rows,
            st.session_state.cols,
            st.session_state.start,
            st.session_state.goal,
        )
    
    # Ejecutar algoritmo
    t0 = time.perf_counter()
    path, nodes, visited = algo.solve()
    elapsed = (time.perf_counter() - t0) * 1000
    
    # Actualizar estado
    st.session_state.visited = visited
    st.session_state.frontier = set()
    st.session_state.path = set(path) if path else set()
    
    result = {
        'algo': algo_name,
        'path': len(path) if path else 'N/A',
        'nodes': nodes,
        'time': elapsed,
    }
    
    st.session_state.last_result = result
    return result


def run_all_algorithms():
    """Ejecuta todos los algoritmos y compara resultados"""
    st.session_state.compare_results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    algos = ['BFS', 'DFS', 'Greedy', 'A*']
    for i, algo in enumerate(algos):
        status_text.text(f"Ejecutando {algo}...")
        reset_maze_state()
        result = run_algorithm(algo)
        
        if result:
            st.session_state.compare_results.append(result)
        
        progress_bar.progress((i + 1) / len(algos))
        time.sleep(0.3)
    
    status_text.success("¡Comparación completada!")


# ═════════════════════════════════════════════════════════════════
#  INTERFAZ
# ═════════════════════════════════════════════════════════════════
def main():
    init_session_state()
    
    # Header
    st.markdown("# Maze Solver")
    st.markdown("**Proyecto #2 IA CC3085** — Algoritmos de busqueda en laberintos")
    st.divider()
    
    # Layout principal
    col_left, col_right = st.columns([1, 3])
    
    # ═════════════════════════════════════════════════════════════
    #  PANEL IZQUIERDO (CONTROLES)
    # ═════════════════════════════════════════════════════════════
    with col_left:
        st.markdown("## Configuracion")
        
        # Cargar laberinto
        st.subheader("Laberinto")
        
        # Opción 1: Cargar archivo
        uploaded_file = st.file_uploader(
            "Cargar archivo .txt",
            type=['txt'],
            help="Archivo de texto con el laberinto"
        )
        
        if uploaded_file is not None:
            try:
                content = StringIO(uploaded_file.getvalue().decode()).read()
                maze, rows, cols, start, goal = load_maze_from_text(content)
                
                if not start or not goal:
                    st.error("Error: El laberinto debe tener inicio (2) y meta (3)")
                else:
                    load_maze_data(maze, rows, cols, start, goal)
                    st.success(f"Laberinto cargado: {rows}x{cols}")
            except Exception as e:
                st.error(f"❌ Error al cargar archivo: {e}")
        
        
        st.divider()
        
        # Algoritmos
        st.subheader("Algoritmo")
        st.session_state.algorithm = st.radio(
            "Selecciona un algoritmo:",
            ["BFS", "DFS", "Greedy", "A*"],
            label_visibility="collapsed",
        )
        
        st.divider()
        
        # Heuristica
        st.subheader("Heuristica")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Manhattan", use_container_width=True):
                st.session_state.heuristic = "manhattan"
        with col2:
            if st.button("Euclidiana", use_container_width=True):
                st.session_state.heuristic = "euclidean"
        
        heuristic_label = "Manhattan" if st.session_state.heuristic == "manhattan" else "Euclidiana"
        st.caption(f"Actual: **{heuristic_label}**")
        
        st.divider()
        
        # Botones de accion
        st.subheader("Acciones")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Ejecutar", use_container_width=True, key="run"):
                if st.session_state.maze:
                    with st.spinner(f"Ejecutando {st.session_state.algorithm}..."):
                        result = run_algorithm(st.session_state.algorithm)
                        if result:
                            st.session_state.results.append(result)
                else:
                    st.warning("Carga un laberinto primero")
        
        with col2:
            if st.button("Comparar todos", use_container_width=True, key="compare"):
                if st.session_state.maze:
                    run_all_algorithms()
                else:
                    st.warning("Carga un laberinto primero")
        
        if st.button("Limpiar", use_container_width=True, key="clear"):
            st.session_state.start = st.session_state.orig_start
            st.session_state.compare_results = []
            reset_maze_state()
            st.rerun()
        
        st.divider()
        
        # Info
        if st.session_state.maze:
            st.markdown("### Info del laberinto")
            st.caption(f"**Dimensiones:** {st.session_state.rows}x{st.session_state.cols}")
            st.caption(f"**Inicio:** {st.session_state.start}")
            st.caption(f"**Meta:** {st.session_state.goal}")
    
    # ═════════════════════════════════════════════════════════════
    #  PANEL DERECHO (VISUALIZACIÓN)
    # ═════════════════════════════════════════════════════════════
    with col_right:
        if st.session_state.maze:
            # Visualizacion del laberinto
            st.markdown("## Laberinto")
            fig = draw_maze_plotly(
                st.session_state.maze,
                st.session_state.visited,
                st.session_state.frontier,
                st.session_state.path,
                st.session_state.start,
                st.session_state.goal,
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Metricas si hay resultado
            if st.session_state.last_result:
                st.markdown("## Resultados")
                
                col1, col2, col3 = st.columns(3)
                result = st.session_state.last_result
                
                metric_card(col1, "Largo del camino", 
                           result['path'] if result['path'] != 'N/A' else 'N/A',
                           '#C8F050')
                metric_card(col2, "Nodos explorados",
                           result['nodes'],
                           '#50C8F0')
                metric_card(col3, "Tiempo (ms)",
                           f"{result['time']:.2f}",
                           '#F05090')
            
            # Comparacion
            if st.session_state.compare_results:
                st.markdown("## Comparacion")
                
                # Crear DataFrame para la tabla
                df_data = []
                for r in st.session_state.compare_results:
                    df_data.append({
                        'Algoritmo': r['algo'],
                        'Camino': r['path'] if r['path'] != 'N/A' else 'N/A',
                        'Nodos': r['nodes'],
                        'Tiempo (ms)': f"{r['time']:.2f}"
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Algoritmo": st.column_config.TextColumn("Algoritmo", width="medium"),
                        "Camino": st.column_config.TextColumn("Camino", width="medium"),
                        "Nodos": st.column_config.NumberColumn("Nodos", width="medium"),
                        "Tiempo (ms)": st.column_config.TextColumn("Tiempo (ms)", width="medium"),
                    }
                )
        
        else:
            st.info(
                "Carga un laberinto usando el panel de la izquierda para comenzar"
            )
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Universidad del Valle de Guatemala")
    with col2:
        st.caption("Curso: Inteligencia Artificial (CC3085)")
    with col3:
        st.caption("Proyecto #2: Maze Solver")


if __name__ == "__main__":
    main()
