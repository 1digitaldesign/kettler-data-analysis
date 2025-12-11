#!/usr/bin/env python3
"""
Graph Theory Analysis - Violation-Form Connection Analysis
Uses graph theory and shortest path algorithms to analyze violation-form connections
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, deque
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import heapq

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR

# Optimize for ARM M4 MAX
MAX_WORKERS = os.cpu_count() or 16
print(f"🚀 Graph Theory Analysis - ARM M4 MAX Optimized ({MAX_WORKERS} workers)")

try:
    import networkx as nx
    print("✅ NetworkX available")
except ImportError:
    print("Installing NetworkX...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "networkx"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import networkx as nx
    print("✅ NetworkX installed")


class GraphTheoryAnalyzer:
    """Graph theory analysis for violation-form connections"""

    def __init__(self):
        self.graph = nx.DiGraph()  # Directed graph
        self.violations = {}
        self.laws = {}
        self.forms = {}
        self.node_metadata = {}
        self.edge_weights = {}

    def load_connections(self, analysis_file: Path):
        """Load connections from advanced ML analysis"""
        print(f"\n📂 Loading connections from {analysis_file}...")

        with open(analysis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Load network structure
        network = data.get("network", {})
        connections = data.get("connections", {})

        # Extract nodes
        nodes = network.get("nodes", {})
        self.violations = nodes.get("violations", {})
        self.laws = nodes.get("laws", {})
        self.forms = nodes.get("forms", {})

        print(f"   Loaded {len(self.violations)} violations")
        print(f"   Loaded {len(self.laws)} laws")
        print(f"   Loaded {len(self.forms)} forms")

        # Build graph from connections
        self._build_graph(connections, network.get("edges", {}))

        print(f"✅ Graph built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")

    def _build_graph(self, connections: Dict[str, List], edges: Dict[str, List]):
        """Build NetworkX graph from connections"""
        print(f"\n🔨 Building graph structure...")

        # Add all nodes with metadata
        for node_id, node_data in self.violations.items():
            # node_data already has 'type' and 'data' keys, use as-is
            if isinstance(node_data, dict):
                # Keep the structure but ensure type is set
                node_attrs = {k: v for k, v in node_data.items() if k != "data"}
                node_attrs["type"] = node_data.get("type", "violation")
                self.graph.add_node(node_id, **node_attrs)
            else:
                self.graph.add_node(node_id, type="violation")
            self.node_metadata[node_id] = {"type": "violation", "data": node_data}

        for node_id, node_data in self.laws.items():
            if isinstance(node_data, dict):
                node_attrs = {k: v for k, v in node_data.items() if k != "data"}
                node_attrs["type"] = node_data.get("type", "law")
                self.graph.add_node(node_id, **node_attrs)
            else:
                self.graph.add_node(node_id, type="law")
            self.node_metadata[node_id] = {"type": "law", "data": node_data}

        for node_id, node_data in self.forms.items():
            if isinstance(node_data, dict):
                node_attrs = {k: v for k, v in node_data.items() if k != "data"}
                node_attrs["type"] = node_data.get("type", "form")
                self.graph.add_node(node_id, **node_attrs)
            else:
                self.graph.add_node(node_id, type="form")
            self.node_metadata[node_id] = {"type": "form", "data": node_data}

        # Add edges from connections (and add missing nodes)
        edge_count = 0

        # Violation-Law edges
        for conn in connections.get("violation_law", []):
            violation = conn.get("violation")
            law = conn.get("law")
            similarity = conn.get("similarity", 0.5)
            if violation and law:
                # Add nodes if they don't exist
                if violation not in self.graph:
                    self.graph.add_node(violation, type="violation")
                if law not in self.graph:
                    self.graph.add_node(law, type="law")

                # Weight is inverse of similarity (lower = better path)
                weight = 1.0 - similarity
                self.graph.add_edge(violation, law,
                                   weight=weight,
                                   similarity=similarity,
                                   connection_type="violation_law")
                self.edge_weights[(violation, law)] = weight
                edge_count += 1

        # Violation-Form edges (direct)
        for conn in connections.get("violation_form", []):
            violation = conn.get("violation")
            form = conn.get("form")
            similarity = conn.get("similarity", 0.5)
            if violation and form:
                # Add nodes if they don't exist
                if violation not in self.graph:
                    self.graph.add_node(violation, type="violation")
                if form not in self.graph:
                    self.graph.add_node(form, type="form")

                weight = 1.0 - similarity
                self.graph.add_edge(violation, form,
                                   weight=weight,
                                   similarity=similarity,
                                   connection_type="violation_form")
                self.edge_weights[(violation, form)] = weight
                edge_count += 1

        # Law-Form edges
        for conn in connections.get("law_form", []):
            law = conn.get("law")
            form = conn.get("form")
            similarity = conn.get("similarity", 0.5)
            if law and form:
                # Add nodes if they don't exist
                if law not in self.graph:
                    self.graph.add_node(law, type="law")
                if form not in self.graph:
                    self.graph.add_node(form, type="form")

                weight = 1.0 - similarity
                self.graph.add_edge(law, form,
                                   weight=weight,
                                   similarity=similarity,
                                   connection_type="law_form")
                self.edge_weights[(law, form)] = weight
                edge_count += 1

        print(f"   Added {edge_count} weighted edges")

    def find_shortest_paths_dijkstra(self, source: str, target: str) -> Optional[List[str]]:
        """Find shortest path using Dijkstra's algorithm"""
        try:
            if source not in self.graph or target not in self.graph:
                return None

            path = nx.shortest_path(self.graph, source, target, weight='weight')
            path_length = nx.shortest_path_length(self.graph, source, target, weight='weight')

            return {
                "path": path,
                "length": path_length,
                "algorithm": "dijkstra"
            }
        except nx.NetworkXNoPath:
            return None

    def find_all_violation_form_paths(self, max_path_length: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """Find all paths from violations to forms using multiple algorithms"""
        print(f"\n🔍 Finding all violation-to-form paths (max length: {max_path_length})...")

        violation_nodes = [n for n in self.graph.nodes() if self.graph.nodes[n].get("type") == "violation"]
        form_nodes = [n for n in self.graph.nodes() if self.graph.nodes[n].get("type") == "form"]

        print(f"   Analyzing {len(violation_nodes)} violations → {len(form_nodes)} forms")
        print(f"   Graph has {self.graph.number_of_edges()} edges")

        # Debug: Check if we have any direct violation-form edges
        direct_edges = sum(1 for u, v in self.graph.edges()
                          if self.graph.nodes[u].get("type") == "violation"
                          and self.graph.nodes[v].get("type") == "form")
        print(f"   Direct violation-form edges: {direct_edges}")

        all_paths = defaultdict(list)

        def find_paths_for_pair(violation, form):
            """Find paths between a violation and form"""
            paths = []

            # Skip if nodes don't exist
            if violation not in self.graph or form not in self.graph:
                return paths

            # 1. Direct path (if exists)
            if self.graph.has_edge(violation, form):
                edge_data = self.graph[violation][form]
                paths.append({
                    "path": [violation, form],
                    "length": 1,
                    "algorithm": "direct",
                    "weight": edge_data.get("weight", 1.0),
                    "similarity": edge_data.get("similarity", 0.0)
                })

            # 2. Dijkstra shortest path
            try:
                dijkstra_path = nx.shortest_path(self.graph, violation, form, weight='weight')
                if len(dijkstra_path) > 1:
                    path_weight = sum(self.graph[dijkstra_path[i]][dijkstra_path[i+1]].get("weight", 1.0)
                                     for i in range(len(dijkstra_path)-1))
                    paths.append({
                        "path": dijkstra_path,
                        "length": len(dijkstra_path) - 1,
                        "algorithm": "dijkstra",
                        "weight": path_weight,
                        "hops": len(dijkstra_path) - 1
                    })
            except (nx.NetworkXNoPath, KeyError, nx.NodeNotFound):
                pass

            # 3. All simple paths (up to max_path_length)
            try:
                simple_paths = list(nx.all_simple_paths(self.graph, violation, form, cutoff=max_path_length))
                for path in simple_paths:
                    if len(path) > 1:
                        path_weight = sum(self.graph[path[i]][path[i+1]].get("weight", 1.0)
                                         for i in range(len(path)-1))
                        paths.append({
                            "path": path,
                            "length": len(path) - 1,
                            "algorithm": "all_simple_paths",
                            "weight": path_weight,
                            "hops": len(path) - 1
                        })
            except (nx.NetworkXNoPath, KeyError, nx.NodeNotFound):
                pass

            return paths

        # Process in parallel batches
        total_pairs = len(violation_nodes) * len(form_nodes)
        processed = 0

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {}
            for violation in violation_nodes:
                for form in form_nodes:
                    future = executor.submit(find_paths_for_pair, violation, form)
                    futures[future] = (violation, form)

            for future in as_completed(futures):
                try:
                    violation_id, form_id = futures[future]
                    paths = future.result()
                    if paths:
                        pair_key = f"{violation_id}→{form_id}"
                        all_paths[pair_key].extend(paths)

                    processed += 1
                    if processed % 100 == 0:
                        print(f"   Progress: {processed}/{total_pairs} pairs analyzed, {len(all_paths)} pairs with paths")
                except Exception as e:
                    print(f"   ⚠️  Error: {e}")
                    import traceback
                    traceback.print_exc()

        print(f"✅ Found paths for {len(all_paths)} violation-form pairs")
        return dict(all_paths)

    def analyze_graph_centrality(self) -> Dict[str, Any]:
        """Analyze graph centrality metrics"""
        print(f"\n📊 Analyzing graph centrality...")

        centrality = {}

        # Degree centrality
        degree_centrality = nx.degree_centrality(self.graph)
        centrality["degree"] = dict(sorted(degree_centrality.items(),
                                          key=lambda x: x[1], reverse=True)[:20])

        # Betweenness centrality (parallel computation)
        print("   Computing betweenness centrality (parallel)...")
        betweenness_centrality = nx.betweenness_centrality(self.graph, weight='weight',
                                                           k=min(100, self.graph.number_of_nodes()))
        centrality["betweenness"] = dict(sorted(betweenness_centrality.items(),
                                              key=lambda x: x[1], reverse=True)[:20])

        # Closeness centrality
        print("   Computing closeness centrality...")
        closeness_centrality = nx.closeness_centrality(self.graph, distance='weight')
        centrality["closeness"] = dict(sorted(closeness_centrality.items(),
                                             key=lambda x: x[1], reverse=True)[:20])

        # PageRank
        print("   Computing PageRank...")
        pagerank = nx.pagerank(self.graph, weight='weight')
        centrality["pagerank"] = dict(sorted(pagerank.items(),
                                           key=lambda x: x[1], reverse=True)[:20])

        print(f"✅ Centrality analysis complete")
        return centrality

    def find_communities(self) -> Dict[str, Any]:
        """Find communities in the graph"""
        print(f"\n🔍 Finding communities...")

        # Convert to undirected for community detection
        undirected_graph = self.graph.to_undirected()

        # Use Louvain algorithm if available, else use greedy modularity
        try:
            import community as community_louvain
            communities = community_louvain.best_partition(undirected_graph)
        except ImportError:
            # Fallback to greedy modularity
            communities = nx.community.greedy_modularity_communities(undirected_graph)
            # Convert to dict format
            communities_dict = {}
            for i, comm in enumerate(communities):
                for node in comm:
                    communities_dict[node] = i
            communities = communities_dict

        # Organize by community
        community_groups = defaultdict(list)
        for node, comm_id in communities.items():
            community_groups[comm_id].append(node)

        print(f"✅ Found {len(community_groups)} communities")
        return {
            "communities": dict(community_groups),
            "n_communities": len(community_groups),
            "modularity": nx.community.modularity(undirected_graph,
                                                  [set(comm) for comm in community_groups.values()])
        }

    def find_optimal_pathways(self, paths: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Find optimal pathways from violations to forms"""
        print(f"\n🎯 Finding optimal pathways...")

        optimal_pathways = {
            "shortest_paths": [],
            "highest_similarity_paths": [],
            "most_common_paths": [],
            "violation_form_matrix": {}
        }

        # Analyze all paths
        path_stats = defaultdict(list)

        for pair_key, path_list in paths.items():
            if not path_list:
                continue

            # Find shortest path (by weight)
            shortest = min(path_list, key=lambda p: p.get("weight", float('inf')))
            optimal_pathways["shortest_paths"].append({
                "pair": pair_key,
                "path": shortest["path"],
                "weight": shortest.get("weight", 0),
                "hops": shortest.get("hops", 0)
            })

            # Find highest similarity path
            highest_sim = max(path_list, key=lambda p: p.get("similarity", 0))
            if highest_sim.get("similarity", 0) > 0:
                optimal_pathways["highest_similarity_paths"].append({
                    "pair": pair_key,
                    "path": highest_sim["path"],
                    "similarity": highest_sim.get("similarity", 0),
                    "hops": highest_sim.get("hops", 0)
                })

            # Track path patterns
            for path_info in path_list:
                path_str = "→".join(path_info["path"])
                path_stats[path_str].append({
                    "pair": pair_key,
                    "weight": path_info.get("weight", 0),
                    "similarity": path_info.get("similarity", 0)
                })

        # Most common paths
        sorted_paths = sorted(path_stats.items(), key=lambda x: len(x[1]), reverse=True)[:20]
        optimal_pathways["most_common_paths"] = [
            {
                "path": path_str,
                "frequency": len(stats),
                "avg_weight": np.mean([s["weight"] for s in stats]),
                "avg_similarity": np.mean([s["similarity"] for s in stats if s["similarity"] > 0])
            }
            for path_str, stats in sorted_paths
        ]

        print(f"✅ Found {len(optimal_pathways['shortest_paths'])} optimal pathways")
        return optimal_pathways

    def generate_pathway_report(self, paths: Dict[str, List],
                               centrality: Dict[str, Any],
                               communities: Dict[str, Any],
                               optimal_pathways: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive pathway analysis report"""
        print(f"\n📊 Generating comprehensive pathway report...")

        report = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "graph_nodes": self.graph.number_of_nodes(),
                "graph_edges": self.graph.number_of_edges(),
                "violations": len(self.violations),
                "laws": len(self.laws),
                "forms": len(self.forms)
            },
            "graph_statistics": {
                "density": nx.density(self.graph),
                "is_connected": nx.is_strongly_connected(self.graph),
                "is_weakly_connected": nx.is_weakly_connected(self.graph),
                "number_of_components": nx.number_weakly_connected_components(self.graph),
                "average_clustering": nx.average_clustering(self.graph.to_undirected())
            },
            "pathways": {
                "total_violation_form_pairs": len(paths),
                "total_paths_found": sum(len(p) for p in paths.values()),
                "direct_paths": sum(1 for p_list in paths.values()
                                  for p in p_list if p.get("length") == 1),
                "indirect_paths": sum(1 for p_list in paths.values()
                                     for p in p_list if p.get("length") > 1)
            },
            "centrality": centrality,
            "communities": communities,
            "optimal_pathways": optimal_pathways,
            "sample_paths": dict(list(paths.items())[:10])  # First 10 for sample
        }

        return report


def main():
    """Main function to run graph theory analysis"""
    import time
    start_time = time.time()

    print("=" * 80)
    print("🔬 Graph Theory Analysis - Violation-Form Connection Analysis")
    print("=" * 80)
    print(f"Architecture: ARM M4 MAX")
    print(f"Workers: {MAX_WORKERS}")
    print("=" * 80)
    print()

    analyzer = GraphTheoryAnalyzer()

    # Load connections
    analysis_file = DATA_PROCESSED_DIR / "advanced_ml_analysis.json"
    if not analysis_file.exists():
        print(f"❌ Analysis file not found: {analysis_file}")
        print("   Please run advanced_ml_pipeline.py first")
        sys.exit(1)

    analyzer.load_connections(analysis_file)

    # Find all violation-form paths
    paths = analyzer.find_all_violation_form_paths(max_path_length=3)

    # Analyze centrality
    centrality = analyzer.analyze_graph_centrality()

    # Find communities
    communities = analyzer.find_communities()

    # Find optimal pathways
    optimal_pathways = analyzer.find_optimal_pathways(paths)

    # Generate report
    report = analyzer.generate_pathway_report(paths, centrality, communities, optimal_pathways)

    # Save results
    output_file = DATA_PROCESSED_DIR / "graph_theory_analysis.json"
    print(f"\n💾 Saving graph theory analysis to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    total_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("✅ Graph Theory Analysis Complete!")
    print("=" * 80)
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Graph: {report['metadata']['graph_nodes']} nodes, {report['metadata']['graph_edges']} edges")
    print(f"Pathways: {report['pathways']['total_paths_found']} paths found")
    print(f"Direct paths: {report['pathways']['direct_paths']}")
    print(f"Indirect paths: {report['pathways']['indirect_paths']}")
    print(f"Communities: {report['communities']['n_communities']}")
    print(f"Optimal pathways: {len(optimal_pathways['shortest_paths'])}")
    print("=" * 80)


if __name__ == "__main__":
    main()
