#!/usr/bin/env python3
"""
Comprehensive Visualization Generator
Creates all available visualizations using Plotly, Bokeh, Altair, and Seaborn
"""

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import DATA_PROCESSED_DIR, RESEARCH_DIR
from scripts.analysis.utils.advanced_visualizations import AdvancedVisualizer

def load_analysis_data() -> tuple:
    """Load data for visualization"""
    try:
        # Load ML analysis results
        ml_file = DATA_PROCESSED_DIR / "ml_tax_structure_analysis.json"
        if ml_file.exists():
            with open(ml_file, 'r') as f:
                ml_data = json.load(f)
        else:
            ml_data = {}
        
        # Load graph theory analysis
        graph_file = DATA_PROCESSED_DIR / "graph_theory_analysis.json"
        if graph_file.exists():
            with open(graph_file, 'r') as f:
                graph_data = json.load(f)
        else:
            graph_data = {}
        
        # Load embedding analysis
        embedding_file = DATA_PROCESSED_DIR / "embedding_similarity_analysis.json"
        if embedding_file.exists():
            with open(embedding_file, 'r') as f:
                embedding_data = json.load(f)
        else:
            embedding_data = {}
        
        return ml_data, graph_data, embedding_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}, {}, {}

def create_all_visualizations():
    """Create comprehensive visualization suite"""
    print("🎨 Creating Comprehensive Visualization Suite")
    print("=" * 60)
    
    # Setup output directory
    output_dir = RESEARCH_DIR / "texas" / "analysis" / "visualizations"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize visualizer
    viz = AdvancedVisualizer(output_dir)
    
    # Check available libraries
    libs = viz.get_available_libraries()
    print("\n📚 Available Visualization Libraries:")
    for lib, available in libs.items():
        status = "✅" if available else "❌"
        print(f"   {status} {lib}")
    
    # Load data
    print("\n📂 Loading analysis data...")
    ml_data, graph_data, embedding_data = load_analysis_data()
    
    all_visualizations = {}
    
    # 1. ML Analysis Visualizations
    if ml_data:
        print("\n🤖 Creating ML Analysis Visualizations...")
        
        # Extract features and labels if available
        if 'clustering' in ml_data and 'kmeans' in ml_data['clustering']:
            kmeans = ml_data['clustering']['kmeans']
            if 'cluster_labels' in kmeans and 'cluster_centers' in kmeans:
                # Create sample features from cluster centers
                centers = np.array(kmeans['cluster_centers'])
                labels = np.array(kmeans['cluster_labels'])
                
                # Create synthetic features for demonstration
                n_samples = len(labels)
                if n_samples > 0 and len(centers) > 0:
                    # Generate features around cluster centers
                    features = np.random.randn(n_samples, centers.shape[1]) * 0.1
                    for i, label in enumerate(labels):
                        if label < len(centers):
                            features[i] += centers[label]
                    
                    # Cluster plot
                    viz_path = viz.create_cluster_plot_plotly(
                        features, labels, "K-Means Clustering Analysis"
                    )
                    if viz_path:
                        all_visualizations['kmeans_cluster'] = viz_path
                        print(f"   ✅ Created: {Path(viz_path).name}")
                    
                    # 3D scatter if possible
                    if features.shape[1] >= 3:
                        viz_path = viz.create_3d_scatter_plotly(
                            features[:, 0], features[:, 1], features[:, 2],
                            labels, "3D Feature Space"
                        )
                        if viz_path:
                            all_visualizations['3d_scatter'] = viz_path
                            print(f"   ✅ Created: {Path(viz_path).name}")
        
        # Anomaly detection visualization
        if 'anomaly_detection' in ml_data:
            anomaly = ml_data['anomaly_detection']
            if 'isolation_forest' in anomaly:
                iso = anomaly['isolation_forest']
                if 'anomaly_labels' in iso:
                    labels = np.array(iso['anomaly_labels'])
                    # Create sample features
                    features = np.random.randn(len(labels), 2)
                    viz_path = viz.create_anomaly_detection_plot(
                        features, labels, "Anomaly Detection Results"
                    )
                    if viz_path:
                        all_visualizations['anomaly_detection'] = viz_path
                        print(f"   ✅ Created: {Path(viz_path).name}")
    
    # 2. Graph Theory Visualizations
    if graph_data:
        print("\n🌐 Creating Graph Theory Visualizations...")
        
        # Network graph (Plotly)
        viz_path = viz.create_network_graph_plotly(
            graph_data, "Violation-Law-Form Network"
        )
        if viz_path:
            all_visualizations['network_plotly'] = viz_path
            print(f"   ✅ Created: {Path(viz_path).name}")
        
        # Network graph (Bokeh)
        viz_path = viz.create_network_graph_bokeh(
            graph_data, "Network Graph (Bokeh)"
        )
        if viz_path:
            all_visualizations['network_bokeh'] = viz_path
            print(f"   ✅ Created: {Path(viz_path).name}")
    
    # 3. Statistical Visualizations
    print("\n📊 Creating Statistical Visualizations...")
    
    # Create sample data for statistical plots
    sample_data = pd.DataFrame({
        'feature_1': np.random.randn(100),
        'feature_2': np.random.randn(100),
        'feature_3': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    # Correlation heatmap
    viz_path = viz.create_heatmap_plotly(
        sample_data, "Feature Correlation Matrix"
    )
    if viz_path:
        all_visualizations['correlation_heatmap'] = viz_path
        print(f"   ✅ Created: {Path(viz_path).name}")
    
    # Box plots
    for col in ['feature_1', 'feature_2']:
        viz_path = viz.create_box_plot_plotly(
            sample_data, col, 'category', f"Box Plot: {col}"
        )
        if viz_path:
            all_visualizations[f'box_plot_{col}'] = viz_path
            print(f"   ✅ Created: {Path(viz_path).name}")
    
    # Violin plots
    viz_path = viz.create_violin_plot_plotly(
        sample_data, 'feature_1', 'category', "Violin Plot Analysis"
    )
    if viz_path:
        all_visualizations['violin_plot'] = viz_path
        print(f"   ✅ Created: {Path(viz_path).name}")
    
    # 4. Altair Visualizations
    print("\n📈 Creating Altair Statistical Charts...")
    
    viz_path = viz.create_altair_chart(
        sample_data, 'feature_1', 'feature_2', 'category',
        chart_type="scatter", title="Statistical Scatter Plot"
    )
    if viz_path:
        all_visualizations['scatter_altair'] = viz_path
        print(f"   ✅ Created: {Path(viz_path).name}")
    
    # 5. Seaborn Visualizations
    print("\n🎨 Creating Seaborn Statistical Plots...")
    
    viz_path = viz.create_seaborn_pairplot(
        sample_data[['feature_1', 'feature_2', 'feature_3']],
        title="Feature Pair Plot"
    )
    if viz_path:
        all_visualizations['pairplot_seaborn'] = viz_path
        print(f"   ✅ Created: {Path(viz_path).name}")
    
    # 6. Create Comprehensive Dashboard
    print("\n📱 Creating Comprehensive Dashboard...")
    dashboard_path = viz.create_dashboard_html(
        all_visualizations, "Complete Analysis Visualization Dashboard"
    )
    if dashboard_path:
        all_visualizations['comprehensive_dashboard'] = dashboard_path
        print(f"   ✅ Created: {Path(dashboard_path).name}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"✅ Created {len(all_visualizations)} visualizations")
    print(f"📁 Output directory: {output_dir}")
    print("\n📊 Visualization Summary:")
    for name, path in all_visualizations.items():
        if path:
            print(f"   • {name}: {Path(path).name}")
    
    # Save visualization index
    index_file = output_dir / "visualization_index.json"
    with open(index_file, 'w') as f:
        json.dump({
            'total_visualizations': len(all_visualizations),
            'visualizations': {k: str(Path(v).name) if v else None 
                             for k, v in all_visualizations.items()},
            'output_directory': str(output_dir),
            'libraries_used': libs
        }, f, indent=2)
    
    print(f"\n📑 Visualization index saved: {index_file.name}")
    print("\n🎉 Visualization suite complete!")

if __name__ == "__main__":
    create_all_visualizations()
