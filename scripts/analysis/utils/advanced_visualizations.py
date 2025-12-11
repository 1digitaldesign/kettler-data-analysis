#!/usr/bin/env python3
"""
Advanced Visualization Utilities using Modern Libraries
Uses Plotly, Bokeh, and Altair for interactive, publication-quality visualizations
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd

# Try importing modern visualization libraries
PLOTLY_AVAILABLE = False
BOKEH_AVAILABLE = False
ALTAIR_AVAILABLE = False
SEABORN_AVAILABLE = False
MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.offline as pyo
    PLOTLY_AVAILABLE = True
except ImportError:
    pass

try:
    from bokeh.plotting import figure, output_file, save, show
    from bokeh.models import HoverTool, ColumnDataSource, ColorBar
    from bokeh.palettes import Category10, Viridis256
    from bokeh.layouts import gridplot, column, row
    BOKEH_AVAILABLE = True
except ImportError:
    pass

try:
    import altair as alt
    ALTAIR_AVAILABLE = True
except ImportError:
    pass

try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    SEABORN_AVAILABLE = True
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    pass


class AdvancedVisualizer:
    """Modern visualization utilities using Plotly, Bokeh, and Altair"""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.available_libs = {
            'plotly': PLOTLY_AVAILABLE,
            'bokeh': BOKEH_AVAILABLE,
            'altair': ALTAIR_AVAILABLE,
            'seaborn': SEABORN_AVAILABLE,
            'matplotlib': MATPLOTLIB_AVAILABLE
        }

    def create_cluster_plot_plotly(self, features: np.ndarray, labels: np.ndarray,
                                   title: str = "K-Means Clustering") -> Optional[str]:
        """Create interactive cluster plot using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        # Reduce to 2D using PCA if needed
        if features.shape[1] > 2:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            features_2d = pca.fit_transform(features)
            x_label = f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)"
            y_label = f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)"
        else:
            features_2d = features
            x_label = "Feature 1"
            y_label = "Feature 2"

        # Create DataFrame for Plotly
        df = pd.DataFrame({
            'x': features_2d[:, 0],
            'y': features_2d[:, 1],
            'cluster': labels.astype(str),
            'index': range(len(labels))
        })

        # Create interactive scatter plot
        fig = px.scatter(
            df, x='x', y='y', color='cluster',
            title=title,
            labels={'x': x_label, 'y': y_label},
            hover_data=['index'],
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        fig.update_traces(
            marker=dict(size=8, opacity=0.7, line=dict(width=1, color='white')),
            selector=dict(mode='markers')
        )

        fig.update_layout(
            template='plotly_white',
            width=1000,
            height=800,
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4'),
            hovermode='closest'
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_network_graph_plotly(self, graph_data: Dict[str, Any],
                                    title: str = "Network Graph") -> Optional[str]:
        """Create interactive network graph using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        try:
            import networkx as nx
            G = nx.Graph()

            # Add nodes and edges from graph_data
            if 'nodes' in graph_data:
                for node in graph_data['nodes']:
                    G.add_node(node.get('id', node))

            if 'edges' in graph_data:
                for edge in graph_data['edges']:
                    G.add_edge(edge.get('source'), edge.get('target'))

            # Use spring layout
            pos = nx.spring_layout(G, k=1, iterations=50)

            # Extract node positions
            node_x = [pos[node][0] for node in G.nodes()]
            node_y = [pos[node][1] for node in G.nodes()]

            # Create edge traces
            edge_traces = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_traces.append(
                    go.Scatter(
                        x=[x0, x1, None], y=[y0, y1, None],
                        mode='lines',
                        line=dict(width=0.5, color='#888'),
                        hoverinfo='none',
                        showlegend=False
                    )
                )

            # Create node trace
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                marker=dict(
                    size=10,
                    color='#1f77b4',
                    line=dict(width=2, color='white')
                ),
                text=list(G.nodes()),
                textposition="middle center",
                hoverinfo='text',
                showlegend=False
            )

            fig = go.Figure(
                data=edge_traces + [node_trace],
                layout=go.Layout(
                    title=title,
                    titlefont=dict(size=18),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="Interactive Network Graph",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002,
                        xanchor="left", yanchor="bottom",
                        font=dict(color="#888", size=12)
                    )],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    template='plotly_white',
                    width=1200,
                    height=800
                )
            )

            output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_network_plotly.html"
            fig.write_html(str(output_path))
            return str(output_path)
        except Exception as e:
            print(f"Error creating network graph: {e}")
            return None

    def create_time_series_plotly(self, data: pd.DataFrame,
                                  x_col: str, y_col: str,
                                  title: str = "Time Series Analysis") -> Optional[str]:
        """Create interactive time series plot using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        fig = px.line(
            data, x=x_col, y=y_col,
            title=title,
            labels={x_col: 'Time', y_col: 'Value'},
            markers=True
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8)
        )

        fig.update_layout(
            template='plotly_white',
            width=1200,
            height=600,
            hovermode='x unified',
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4')
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_timeseries_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_anomaly_detection_plot(self, features: np.ndarray,
                                     anomaly_labels: np.ndarray,
                                     title: str = "Anomaly Detection") -> Optional[str]:
        """Create interactive anomaly detection visualization"""
        if not PLOTLY_AVAILABLE:
            return None

        # Reduce to 2D
        if features.shape[1] > 2:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            features_2d = pca.fit_transform(features)
        else:
            features_2d = features

        df = pd.DataFrame({
            'x': features_2d[:, 0],
            'y': features_2d[:, 1],
            'anomaly': ['Anomaly' if label == -1 else 'Normal' for label in anomaly_labels],
            'index': range(len(anomaly_labels))
        })

        fig = px.scatter(
            df, x='x', y='y', color='anomaly',
            title=title,
            color_discrete_map={'Anomaly': '#ef4444', 'Normal': '#10b981'},
            hover_data=['index'],
            symbol='anomaly',
            symbol_map={'Anomaly': 'x', 'Normal': 'circle'}
        )

        fig.update_traces(
            marker=dict(size=10, opacity=0.7, line=dict(width=1, color='white')),
            selector=dict(mode='markers')
        )

        fig.update_layout(
            template='plotly_white',
            width=1000,
            height=800,
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4')
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_anomaly_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_dashboard_html(self, visualizations: Dict[str, str],
                             title: str = "ML Analysis Dashboard") -> str:
        """Create an HTML dashboard with all visualizations"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #1f77b4;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        .viz-container {{
            margin: 30px 0;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            background: #fafafa;
        }}
        .viz-container h2 {{
            color: #333;
            margin-top: 0;
        }}
        iframe {{
            width: 100%;
            height: 800px;
            border: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>{title}</h1>
"""

        for viz_name, viz_path in visualizations.items():
            if viz_path:
                html_content += f"""
        <div class="viz-container">
            <h2>{viz_name}</h2>
            <iframe src="{Path(viz_path).name}"></iframe>
        </div>
"""

        html_content += """
    </div>
</body>
</html>
"""

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_dashboard.html"
        with open(output_path, 'w') as f:
            f.write(html_content)

        return str(output_path)

    def get_available_libraries(self) -> Dict[str, bool]:
        """Return status of available visualization libraries"""
        return self.available_libs.copy()
