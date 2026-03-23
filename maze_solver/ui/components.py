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
    """Crea una tarjeta de metrica"""
    with col:
        st.markdown(f"""
        <div style='background: #1a1a1a; border: 1px solid #2a2a2a; 
                    border-radius: 8px; padding: 15px;'>
            <p style='color: #6B6B65; margin: 0; font-size: 12px;'>{label}</p>
            <p style='color: {color}; margin: 5px 0 0 0; 
                       font-size: 24px; font-weight: bold;'>{value}</p>
        </div>
        """, unsafe_allow_html=True)


__all__ = ['draw_maze_plotly', 'metric_card']
