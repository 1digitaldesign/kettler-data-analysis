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

    def create_heatmap_plotly(self, data: pd.DataFrame,
                             title: str = "Correlation Heatmap") -> Optional[str]:
        """Create interactive correlation heatmap using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        # Calculate correlation matrix
        corr_matrix = data.corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))

        fig.update_layout(
            title=title,
            width=1000,
            height=800,
            template='plotly_white',
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4')
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_heatmap_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_3d_scatter_plotly(self, x: np.ndarray, y: np.ndarray, z: np.ndarray,
                                 labels: Optional[np.ndarray] = None,
                                 title: str = "3D Scatter Plot") -> Optional[str]:
        """Create interactive 3D scatter plot using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        if labels is None:
            labels = np.zeros(len(x))

        df = pd.DataFrame({
            'x': x,
            'y': y,
            'z': z,
            'label': labels.astype(str)
        })

        fig = px.scatter_3d(
            df, x='x', y='y', z='z', color='label',
            title=title,
            labels={'x': 'X Axis', 'y': 'Y Axis', 'z': 'Z Axis'},
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        fig.update_traces(
            marker=dict(size=5, opacity=0.7)
        )

        fig.update_layout(
            template='plotly_white',
            width=1200,
            height=800,
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            )
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_3d_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_box_plot_plotly(self, data: pd.DataFrame,
                               value_col: str, category_col: str,
                               title: str = "Box Plot Analysis") -> Optional[str]:
        """Create interactive box plot using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        fig = px.box(
            data, x=category_col, y=value_col,
            title=title,
            color=category_col,
            points="all"
        )

        fig.update_layout(
            template='plotly_white',
            width=1200,
            height=600,
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4')
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_box_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_violin_plot_plotly(self, data: pd.DataFrame,
                                  value_col: str, category_col: str,
                                  title: str = "Violin Plot Analysis") -> Optional[str]:
        """Create interactive violin plot using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        fig = px.violin(
            data, x=category_col, y=value_col,
            title=title,
            color=category_col,
            box=True,
            points="all"
        )

        fig.update_layout(
            template='plotly_white',
            width=1200,
            height=600,
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4')
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_violin_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_sunburst_plotly(self, data: pd.DataFrame,
                               path_cols: List[str], value_col: str,
                               title: str = "Sunburst Chart") -> Optional[str]:
        """Create interactive sunburst chart using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        fig = px.sunburst(
            data, path=path_cols, values=value_col,
            title=title,
            color=value_col,
            color_continuous_scale='Viridis'
        )

        fig.update_layout(
            template='plotly_white',
            width=1000,
            height=1000,
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4')
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_sunburst_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_treemap_plotly(self, data: pd.DataFrame,
                              path_cols: List[str], value_col: str,
                              title: str = "Treemap Chart") -> Optional[str]:
        """Create interactive treemap chart using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        fig = px.treemap(
            data, path=path_cols, values=value_col,
            title=title,
            color=value_col,
            color_continuous_scale='Viridis'
        )

        fig.update_layout(
            template='plotly_white',
            width=1200,
            height=800,
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4')
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_treemap_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_parallel_coordinates_plotly(self, data: pd.DataFrame,
                                           color_col: str,
                                           title: str = "Parallel Coordinates") -> Optional[str]:
        """Create interactive parallel coordinates plot using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        fig = px.parallel_coordinates(
            data, color=color_col,
            title=title,
            color_continuous_scale='Viridis'
        )

        fig.update_layout(
            template='plotly_white',
            width=1400,
            height=600,
            font=dict(family="Arial", size=12),
            title_font=dict(size=18, color='#1f77b4')
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_parallel_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_sankey_diagram_plotly(self, source: List[str], target: List[str],
                                     value: List[float],
                                     title: str = "Sankey Diagram") -> Optional[str]:
        """Create interactive Sankey diagram using Plotly"""
        if not PLOTLY_AVAILABLE:
            return None

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=list(set(source + target)),
                color="blue"
            ),
            link=dict(
                source=[list(set(source + target)).index(s) for s in source],
                target=[list(set(source + target)).index(t) for t in target],
                value=value
            )
        )])

        fig.update_layout(
            title=title,
            font=dict(size=12),
            width=1200,
            height=800,
            template='plotly_white'
        )

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_sankey_plotly.html"
        fig.write_html(str(output_path))
        return str(output_path)

    def create_bokeh_scatter(self, x: np.ndarray, y: np.ndarray,
                            labels: Optional[np.ndarray] = None,
                            title: str = "Bokeh Scatter Plot") -> Optional[str]:
        """Create interactive scatter plot using Bokeh"""
        if not BOKEH_AVAILABLE:
            return None

        from bokeh.plotting import figure, output_file, save
        from bokeh.models import HoverTool, ColumnDataSource

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_bokeh.html"
        output_file(str(output_path))

        if labels is None:
            labels = np.zeros(len(x))

        source = ColumnDataSource(data=dict(
            x=x,
            y=y,
            label=labels.astype(str)
        ))

        p = figure(
            title=title,
            width=1000,
            height=800,
            tools="pan,wheel_zoom,box_zoom,reset,hover,save"
        )

        p.scatter('x', 'y', source=source, size=8, alpha=0.7, color='blue')

        p.add_tools(HoverTool(tooltips=[
            ("x", "@x"),
            ("y", "@y"),
            ("label", "@label")
        ]))

        save(p)
        return str(output_path)

    def create_altair_chart(self, data: pd.DataFrame,
                           x_col: str, y_col: str, color_col: Optional[str] = None,
                           chart_type: str = "scatter",
                           title: str = "Altair Chart") -> Optional[str]:
        """Create declarative statistical visualization using Altair"""
        if not ALTAIR_AVAILABLE:
            return None

        if chart_type == "scatter":
            chart = alt.Chart(data).mark_circle(size=60).encode(
                x=x_col,
                y=y_col,
                color=color_col if color_col else alt.value('steelblue'),
                tooltip=[x_col, y_col]
            ).properties(
                width=800,
                height=600,
                title=title
            )
        elif chart_type == "bar":
            chart = alt.Chart(data).mark_bar().encode(
                x=x_col,
                y=y_col,
                color=color_col if color_col else alt.value('steelblue')
            ).properties(
                width=800,
                height=600,
                title=title
            )
        elif chart_type == "line":
            chart = alt.Chart(data).mark_line().encode(
                x=x_col,
                y=y_col,
                color=color_col if color_col else alt.value('steelblue')
            ).properties(
                width=800,
                height=600,
                title=title
            )
        else:
            return None

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_altair.json"
        chart.save(str(output_path))

        # Also save as HTML
        html_path = self.output_dir / f"{title.lower().replace(' ', '_')}_altair.html"
        chart.save(str(html_path))
        return str(html_path)

    def create_seaborn_pairplot(self, data: pd.DataFrame,
                                hue_col: Optional[str] = None,
                                title: str = "Pair Plot") -> Optional[str]:
        """Create statistical pair plot using Seaborn"""
        if not SEABORN_AVAILABLE:
            return None

        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 10))
        g = sns.pairplot(data, hue=hue_col, diag_kind='kde')
        g.fig.suptitle(title, y=1.02)

        output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_seaborn.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return str(output_path)

    def create_network_graph_bokeh(self, graph_data: Dict[str, Any],
                                   title: str = "Network Graph (Bokeh)") -> Optional[str]:
        """Create interactive network graph using Bokeh"""
        if not BOKEH_AVAILABLE:
            return None

        try:
            import networkx as nx
            from bokeh.plotting import figure, output_file, save
            from bokeh.models import HoverTool, ColumnDataSource
            from bokeh.palettes import Category10

            G = nx.Graph()

            if 'nodes' in graph_data:
                for node in graph_data['nodes']:
                    G.add_node(node.get('id', node))

            if 'edges' in graph_data:
                for edge in graph_data['edges']:
                    G.add_edge(edge.get('source'), edge.get('target'))

            pos = nx.spring_layout(G, k=1, iterations=50)

            output_path = self.output_dir / f"{title.lower().replace(' ', '_')}_bokeh.html"
            output_file(str(output_path))

            p = figure(
                title=title,
                width=1200,
                height=800,
                tools="pan,wheel_zoom,box_zoom,reset,hover,save"
            )

            # Add edges
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                p.line([x0, x1], [y0, y1], line_width=1, color='gray', alpha=0.3)

            # Add nodes
            node_x = [pos[node][0] for node in G.nodes()]
            node_y = [pos[node][1] for node in G.nodes()]

            source = ColumnDataSource(data=dict(
                x=node_x,
                y=node_y,
                node=list(G.nodes())
            ))

            p.scatter('x', 'y', source=source, size=15, color='blue', alpha=0.7)

            save(p)
            return str(output_path)
        except Exception as e:
            print(f"Error creating Bokeh network graph: {e}")
            return None

    def create_dash_dashboard(self, visualizations: Dict[str, str],
                             title: str = "Interactive Dashboard") -> Optional[str]:
        """Create interactive Dash web dashboard"""
        if not PLOTLY_AVAILABLE:
            return None

        try:
            import dash
            from dash import dcc, html
            import dash_bootstrap_components as dbc

            app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

            app.layout = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H1(title, className="text-center mb-4")
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Iframe(
                            src=Path(viz_path).name,
                            style={"width": "100%", "height": "800px", "border": "none"}
                        )
                    ]) for viz_name, viz_path in visualizations.items() if viz_path
                ])
            ], fluid=True)

            # Note: This would need to be run as a server
            # For now, we'll create a simple HTML wrapper
            return self.create_dashboard_html(visualizations, title)
        except Exception as e:
            print(f"Dash dashboard creation: {e}")
            return self.create_dashboard_html(visualizations, title)

    def get_available_libraries(self) -> Dict[str, bool]:
        """Return status of available visualization libraries"""
        return self.available_libs.copy()

    def create_comprehensive_visualization_suite(self, data: pd.DataFrame,
                                                features: Optional[np.ndarray] = None,
                                                labels: Optional[np.ndarray] = None,
                                                graph_data: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Create a comprehensive suite of visualizations using all available libraries"""
        visualizations = {}

        # Plotly visualizations
        if PLOTLY_AVAILABLE and features is not None and labels is not None:
            visualizations['cluster_plotly'] = self.create_cluster_plot_plotly(
                features, labels, "Comprehensive Cluster Analysis"
            )

            if features.shape[1] >= 3:
                visualizations['3d_scatter_plotly'] = self.create_3d_scatter_plotly(
                    features[:, 0], features[:, 1], features[:, 2], labels,
                    "3D Feature Space"
                )

        # Correlation heatmap
        if PLOTLY_AVAILABLE and not data.empty:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                visualizations['heatmap_plotly'] = self.create_heatmap_plotly(
                    data[numeric_cols], "Feature Correlation Matrix"
                )

        # Box plots
        if PLOTLY_AVAILABLE and not data.empty:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
                    visualizations[f'box_plot_{col}_plotly'] = self.create_box_plot_plotly(
                        data, col, data.columns[0] if len(data.columns) > 0 else None,
                        f"Box Plot: {col}"
                    )

        # Network graphs
        if graph_data:
            visualizations['network_plotly'] = self.create_network_graph_plotly(
                graph_data, "Entity Relationship Network"
            )
            if BOKEH_AVAILABLE:
                visualizations['network_bokeh'] = self.create_network_graph_bokeh(
                    graph_data, "Network Graph (Bokeh)"
                )

        # Altair charts
        if ALTAIR_AVAILABLE and not data.empty:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                visualizations['scatter_altair'] = self.create_altair_chart(
                    data, numeric_cols[0], numeric_cols[1],
                    chart_type="scatter", title="Statistical Scatter Plot"
                )

        # Seaborn pair plot
        if SEABORN_AVAILABLE and not data.empty:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                visualizations['pairplot_seaborn'] = self.create_seaborn_pairplot(
                    data[numeric_cols[:5]], title="Feature Pair Plot"
                )

        return visualizations
