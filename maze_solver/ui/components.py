"""
Componentes visuales para la interfaz de Streamlit
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from maze_solver.utils.constants import COLORS


def draw_maze_plotly(maze, visited, frontier, path, start, goal):
    """
    Dibuja un laberinto interactivo usando Plotly
    
    Returns:
        plotly Figure object
    """
    rows = len(maze)
    cols = len(maze[0]) if maze else 0
    
    # Crear matriz de colores
    color_map = np.zeros((rows, cols, 3), dtype=int)
    
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 1:  # Pared
                color_map[r][c] = [26, 26, 26]
            elif (r, c) == start:
                color_map[r][c] = [200, 240, 80]
            elif (r, c) == goal:
                color_map[r][c] = [240, 80, 144]
            elif (r, c) in path:
                color_map[r][c] = [80, 200, 240]
            elif (r, c) in frontier:
                color_map[r][c] = [32, 128, 64]
            elif (r, c) in visited:
                color_map[r][c] = [32, 64, 96]
            else:
                color_map[r][c] = [17, 17, 17]
    
    # Convertir a imagen (valores 0-255)
    color_map = color_map.astype(np.uint8)
    
    fig = go.Figure(data=go.Image(z=color_map))
    fig.update_layout(
        height=600,
        showlegend=False,
        hovermode='closest',
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_zeroline=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    return fig


def metric_card(col, label, value, color):
    """Crea una tarjeta de métrica"""
    with col:
        st.markdown(f"""
        <div style='background: #1a1a1a; border: 1px solid #2a2a2a; 
                    border-radius: 8px; padding: 15px;'>
            <p style='color: #6B6B65; margin: 0; font-size: 12px;'>{label}</p>
            <p style='color: {color}; margin: 5px 0 0 0; 
                       font-size: 24px; font-weight: bold;'>{value}</p>
        </div>
        """, unsafe_allow_html=True)


def comparison_table(results):
    """Crea una tabla de comparación de resultados"""
    if not results:
        return None
    
    valid_results = [r for r in results if r['path'] != 'N/A']
    if not valid_results:
        st.warning("No hay resultados válidos para mostrar")
        return
    
    best_path = min(r['path'] for r in valid_results)
    best_nodes = min(r['nodes'] for r in valid_results)
    best_time = min(r['time'] for r in valid_results)
    
    # Crear tabla HTML
    rows_html = ""
    for r in results:
        path_str = str(r['path']) if r['path'] != 'N/A' else 'N/A'
        path_best = path_str != 'N/A' and r['path'] == best_path
        nodes_best = r['nodes'] == best_nodes
        time_best = abs(r['time'] - best_time) < 0.01
        
        path_color = '#C8F050' if path_best else '#E8E8E0'
        nodes_color = '#C8F050' if nodes_best else '#E8E8E0'
        time_color = '#C8F050' if time_best else '#E8E8E0'
        
        rows_html += f"""
        <tr>
            <td style='padding: 8px; border-bottom: 1px solid #2a2a2a;'>{r['algo']}</td>
            <td style='color: {path_color}; padding: 8px; border-bottom: 1px solid #2a2a2a;'>{path_str}</td>
            <td style='color: {nodes_color}; padding: 8px; border-bottom: 1px solid #2a2a2a;'>{r['nodes']}</td>
            <td style='color: {time_color}; padding: 8px; border-bottom: 1px solid #2a2a2a;'>{r['time']:.2f}ms</td>
        </tr>
        """
    
    html = f"""
    <table style='width: 100%; border-collapse: collapse; font-size: 12px;'>
        <tr style='background: #1a1a1a;'>
            <th style='padding: 8px; border-bottom: 2px solid #2a2a2a; color: #6B6B65;'>ALGO</th>
            <th style='padding: 8px; border-bottom: 2px solid #2a2a2a; color: #6B6B65;'>CAMINO</th>
            <th style='padding: 8px; border-bottom: 2px solid #2a2a2a; color: #6B6B65;'>NODOS</th>
            <th style='padding: 8px; border-bottom: 2px solid #2a2a2a; color: #6B6B65;'>TIEMPO</th>
        </tr>
        {rows_html}
    </table>
    """
    
    st.markdown(html, unsafe_allow_html=True)


__all__ = ['draw_maze_plotly', 'metric_card', 'comparison_table']
