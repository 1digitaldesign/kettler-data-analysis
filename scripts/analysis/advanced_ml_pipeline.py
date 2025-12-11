#!/usr/bin/env python3
"""
Advanced ML Pipeline with TensorFlow-style Parallel Processing
Uses embedded vectors to analyze connections between violations, forms, and laws
Creates ground truth network of relationships
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import multiprocessing as mp

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, DATA_VECTORS_DIR, RESEARCH_DIR

# Optimize for ARM M4 MAX with 128GB RAM
MAX_WORKERS = os.cpu_count() or 16
BATCH_SIZE = 128  # Large batches for 128GB RAM
print(f"🚀 Advanced ML Pipeline - ARM M4 MAX Optimized")
print(f"   Workers: {MAX_WORKERS}, Batch Size: {BATCH_SIZE}, RAM: 128GB")

try:
    from sentence_transformers import SentenceTransformer
    import tensorflow as tf
    print("✅ TensorFlow available for parallel operations")
except ImportError:
    print("Installing TensorFlow and dependencies...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user",
                              "tensorflow-macos", "sentence-transformers", "scikit-learn", "numpy"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import tensorflow as tf
        from sentence_transformers import SentenceTransformer
        print("✅ TensorFlow installed")
    except:
        print("⚠️  TensorFlow installation failed, using NumPy operations")
        tf = None
        from sentence_transformers import SentenceTransformer

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import DBSCAN
    from sklearn.decomposition import PCA
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user",
                          "scikit-learn"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import DBSCAN
    from sklearn.decomposition import PCA


class AdvancedMLPipeline:
    """Advanced ML pipeline with TensorFlow-style parallel processing and vector analysis"""

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.violations = {}
        self.laws = {}
        self.forms = {}
        self.connections = defaultdict(list)
        self.vector_cache = {}  # Leverage 128GB RAM for caching

        # Configure TensorFlow for ARM M4 MAX if available
        if tf is not None:
            tf.config.threading.set_inter_op_parallelism_threads(MAX_WORKERS)
            tf.config.threading.set_intra_op_parallelism_threads(MAX_WORKERS)
            print(f"✅ TensorFlow configured for {MAX_WORKERS} threads")

    def load_all_data(self):
        """Load all data sources in parallel"""
        print("\n📂 Loading all data sources in parallel...")

        def load_file(file_path, name):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return name, json.load(f)
            except Exception as e:
                return name, None

        # Collect all files to load
        files_to_load = [
            (DATA_PROCESSED_DIR / "integrated_violations.json", "violations"),
            (PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json", "laws"),
            (DATA_VECTORS_DIR / "lariat_tx_embeddings.json", "lariat_embeddings"),
        ]

        # Load in parallel
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(load_file, path, name): name for path, name in files_to_load}

            for future in as_completed(futures):
                name, data = future.result()
                if data:
                    if name == "violations":
                        self.violations = data
                    elif name == "laws":
                        self.laws = data
                    elif name == "lariat_embeddings":
                        self.lariat_embeddings = data
                    print(f"   ✅ Loaded {name}")

        print(f"✅ Data loading complete")

    def extract_all_embeddings_parallel(self) -> Dict[str, np.ndarray]:
        """Extract all embeddings in parallel batches (leverage 128GB RAM)"""
        print("\n🔍 Extracting all embeddings in parallel batches...")

        all_embeddings = {}
        all_texts = []
        all_ids = []

        # Collect all texts that need embeddings
        def collect_texts(data, prefix="", collected_ids=None):
            if collected_ids is None:
                collected_ids = set()
            texts = []
            ids = []

            if isinstance(data, dict):
                # Extract law ground truth embeddings (use existing if available, else create new)
                if "ground_truth_embedding" in data and "ground_truth_text" in data:
                    law_id = f"law_{prefix}"
                    if law_id not in collected_ids:
                        texts.append(data["ground_truth_text"])
                        ids.append(law_id)
                        collected_ids.add(law_id)
                elif "name" in data and ("key_sections" in data or "description" in data):
                    # Create text for laws without ground truth embeddings
                    law_text = self._create_law_text(data, prefix)
                    law_id = f"law_{prefix}"
                    if law_id not in collected_ids and law_text:
                        texts.append(law_text)
                        ids.append(law_id)
                        collected_ids.add(law_id)

                # Extract violation texts
                if "violations" in data:
                    for category, items in data["violations"].items():
                        for idx, item in enumerate(items):
                            violation_text = self._create_violation_text(item)
                            violation_id = f"violation_{category}_{item.get('entity_name', 'unknown')}_{idx}"
                            if violation_id not in collected_ids:
                                texts.append(violation_text)
                                ids.append(violation_id)
                                collected_ids.add(violation_id)

                # Extract form texts
                if "reporting_forms" in data:
                    for idx, form in enumerate(data["reporting_forms"]):
                        form_text = self._create_form_text(form)
                        form_id = f"form_{form.get('form_number', form.get('form_name', 'unknown'))}_{idx}"
                        if form_id not in collected_ids:
                            texts.append(form_text)
                            ids.append(form_id)
                            collected_ids.add(form_id)

                # Recursively process
                for key, value in data.items():
                    if key not in ["ground_truth_embedding", "ground_truth_text", "embedding", "embedding_text"]:
                        sub_texts, sub_ids = collect_texts(value, f"{prefix}.{key}" if prefix else key, collected_ids)
                        texts.extend(sub_texts)
                        ids.extend(sub_ids)

            elif isinstance(data, list):
                for i, item in enumerate(data):
                    sub_texts, sub_ids = collect_texts(item, f"{prefix}[{i}]", collected_ids)
                    texts.extend(sub_texts)
                    ids.extend(sub_ids)

            return texts, ids

        # Collect all texts
        all_texts, all_ids = collect_texts(self.violations)
        law_texts, law_ids = collect_texts(self.laws)
        all_texts.extend(law_texts)
        all_ids.extend(law_ids)

        print(f"   Found {len(all_texts)} items requiring embeddings")

        # Batch encode all texts at once (leverage 128GB RAM)
        print(f"   Encoding in batches of {BATCH_SIZE}...")
        embeddings = self.model.encode(all_texts, normalize_embeddings=True,
                                      batch_size=BATCH_SIZE, show_progress_bar=False)

        # Store in cache
        for i, item_id in enumerate(all_ids):
            self.vector_cache[item_id] = embeddings[i]
            all_embeddings[item_id] = embeddings[i]

        print(f"✅ Extracted {len(all_embeddings)} embeddings")
        return all_embeddings

    def _create_violation_text(self, violation: Dict[str, Any]) -> str:
        """Create comprehensive text for violation embedding"""
        parts = []
        parts.append(f"VIOLATION_TYPE: {violation.get('violation_type', '')}")
        parts.append(f"ENTITY: {violation.get('entity_name', '')}")
        parts.append(f"DESCRIPTION: {violation.get('description', '')}")
        parts.append(f"SEVERITY: {violation.get('severity', '')}")
        if violation.get('jurisdiction'):
            parts.append(f"JURISDICTION: {violation['jurisdiction']}")
        if violation.get('state'):
            parts.append(f"STATE: {violation['state']}")
        return " | ".join(parts)

    def _create_form_text(self, form: Dict[str, Any]) -> str:
        """Create comprehensive text for form embedding"""
        parts = []
        parts.append(f"FORM_NAME: {form.get('form_name', '')}")
        parts.append(f"FORM_NUMBER: {form.get('form_number', '')}")
        parts.append(f"AGENCY: {form.get('agency', '')}")
        parts.append(f"DESCRIPTION: {form.get('description', '')}")
        parts.append(f"FORM_TYPE: {form.get('form_type', '')}")
        if form.get('url'):
            parts.append(f"URL: {form['url']}")
        return " | ".join(parts)

    def _create_law_text(self, law_data: Dict[str, Any], path: str = "") -> str:
        """Create comprehensive text for law embedding"""
        parts = []
        if law_data.get("name"):
            parts.append(f"LAW: {law_data['name']}")
        if law_data.get("description"):
            parts.append(f"DESCRIPTION: {law_data['description']}")
        if law_data.get("url"):
            parts.append(f"URL: {law_data['url']}")
        if law_data.get("key_sections"):
            parts.append(f"SECTIONS: {'; '.join(law_data['key_sections'])}")
        if law_data.get("relevance"):
            parts.append(f"RELEVANCE: {law_data['relevance']}")
        return " | ".join(parts)

    def find_connections_parallel(self, embeddings: Dict[str, np.ndarray],
                                 threshold: float = 0.5) -> Dict[str, List[Dict[str, Any]]]:
        """Find connections between violations, forms, and laws using parallel vector operations"""
        print(f"\n🔗 Finding connections using parallel vector analysis (threshold: {threshold})...")
        print(f"   Using adaptive thresholds for ground truth matching...")

        # Separate embeddings by type
        violation_embeddings = {k: v for k, v in embeddings.items() if k.startswith("violation_")}
        law_embeddings = {k: v for k, v in embeddings.items() if k.startswith("law_")}
        form_embeddings = {k: v for k, v in embeddings.items() if k.startswith("form_")}

        print(f"   Violations: {len(violation_embeddings)}")
        print(f"   Laws: {len(law_embeddings)}")
        print(f"   Forms: {len(form_embeddings)}")

        connections = {
            "violation_law": [],
            "violation_form": [],
            "law_form": [],
            "violation_violation": []
        }

        # Use TensorFlow-style batch operations if available, else NumPy
        if tf is not None:
            # Convert to TensorFlow tensors for parallel operations
            violation_tensors = {k: tf.constant(v) for k, v in violation_embeddings.items()}
            law_tensors = {k: tf.constant(v) for k, v in law_embeddings.items()}
            form_tensors = {k: tf.constant(v) for k, v in form_embeddings.items()}

            # Batch compute similarities using TensorFlow
            print("   Using TensorFlow for parallel similarity computation...")

            # Violation-Law connections
            if violation_tensors and law_tensors:
                violation_matrix = tf.stack(list(violation_tensors.values()))
                law_matrix = tf.stack(list(law_tensors.values()))

                # Compute cosine similarity in parallel
                violation_norm = tf.nn.l2_normalize(violation_matrix, axis=1)
                law_norm = tf.nn.l2_normalize(law_matrix, axis=1)
                similarity_matrix = tf.matmul(violation_norm, law_norm, transpose_b=True)

                # Get results
                similarity_np = similarity_matrix.numpy()
                violation_keys = list(violation_tensors.keys())
                law_keys = list(law_tensors.keys())

                for i, v_key in enumerate(violation_keys):
                    for j, l_key in enumerate(law_keys):
                        similarity = float(similarity_np[i, j])
                        if similarity >= threshold:
                            connections["violation_law"].append({
                                "violation": v_key,
                                "law": l_key,
                                "similarity": similarity,
                                "connection_type": "violation_law"
                            })
        else:
            # Fallback to NumPy with parallel processing
            print("   Using NumPy with parallel processing...")

            def compute_violation_law_batch(batch_violations, law_embeddings_dict, threshold_val):
                """Compute similarities for a batch of violations"""
                batch_results = []
                violation_array = np.array([v for v in batch_violations.values()])
                law_array = np.array([v for v in law_embeddings_dict.values()])

                similarities = cosine_similarity(violation_array, law_array)

                violation_keys = list(batch_violations.keys())
                law_keys = list(law_embeddings_dict.keys())

                for i, v_key in enumerate(violation_keys):
                    # Get top matches per violation (not just above threshold)
                    violation_sims = similarities[i]
                    top_indices = np.argsort(violation_sims)[-5:][::-1]  # Top 5 matches

                    for j in top_indices:
                        similarity = float(violation_sims[j])
                        l_key = law_keys[j]  # Get law key from index
                        # Use lower threshold for ground truth matching
                        if similarity >= max(0.5, threshold_val - 0.15):
                            batch_results.append({
                                "violation": v_key,
                                "law": l_key,
                                "similarity": similarity,
                                "connection_type": "violation_law"
                            })
                return batch_results

            # Process violations in parallel batches
            violation_items = list(violation_embeddings.items())
            batch_size = max(1, len(violation_items) // MAX_WORKERS)

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = []
                for i in range(0, len(violation_items), batch_size):
                    batch = dict(violation_items[i:i+batch_size])
                    futures.append(executor.submit(compute_violation_law_batch, batch, law_embeddings, threshold))

                completed = 0
                for future in as_completed(futures):
                    try:
                        batch_results = future.result()
                        connections["violation_law"].extend(batch_results)
                        completed += 1
                        if completed % 5 == 0:
                            print(f"   Progress: {completed} batches processed, {len(connections['violation_law'])} connections found")
                    except Exception as e:
                        print(f"   ⚠️  Error in batch: {e}")

        # Violation-Form connections (parallel with lower threshold)
        violation_form_threshold = max(0.5, threshold - 0.1)
        if violation_embeddings and form_embeddings:
            violation_array = np.array([v for v in violation_embeddings.values()])
            form_array = np.array([v for v in form_embeddings.values()])
            similarities = cosine_similarity(violation_array, form_array)

            violation_keys = list(violation_embeddings.keys())
            form_keys = list(form_embeddings.keys())

            # Process in parallel batches
            def process_violation_form_batch(batch_indices, violation_keys_list, form_keys_list, similarities_matrix):
                batch_connections = []
                for i in batch_indices:
                    v_key = violation_keys_list[i]
                    violation_similarities = similarities_matrix[i]
                    top_indices = np.argsort(violation_similarities)[-3:][::-1]

                    for j in top_indices:
                        similarity = float(violation_similarities[j])
                        if similarity >= violation_form_threshold:
                            batch_connections.append({
                                "violation": v_key,
                                "form": form_keys_list[j],
                                "similarity": similarity,
                                "connection_type": "violation_form"
                            })
                return batch_connections

            batch_size = max(1, len(violation_keys) // MAX_WORKERS)
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = []
                for i in range(0, len(violation_keys), batch_size):
                    batch_indices = list(range(i, min(i+batch_size, len(violation_keys))))
                    futures.append(executor.submit(process_violation_form_batch, batch_indices,
                                                  violation_keys, form_keys, similarities))

                for future in as_completed(futures):
                    try:
                        batch_connections = future.result()
                        connections["violation_form"].extend(batch_connections)
                    except Exception:
                        pass

        # Law-Form connections
        if law_embeddings and form_embeddings:
            law_array = np.array([v for v in law_embeddings.values()])
            form_array = np.array([v for v in form_embeddings.values()])
            similarities = cosine_similarity(law_array, form_array)

            law_keys = list(law_embeddings.keys())
            form_keys = list(form_embeddings.keys())

            for i, l_key in enumerate(law_keys):
                for j, f_key in enumerate(form_keys):
                    similarity = float(similarities[i, j])
                    if similarity >= threshold:
                        connections["law_form"].append({
                            "law": l_key,
                            "form": f_key,
                            "similarity": similarity,
                            "connection_type": "law_form"
                        })

        # Violation-Violation connections (find similar violations)
        if len(violation_embeddings) > 1:
            violation_array = np.array([v for v in violation_embeddings.values()])
            similarities = cosine_similarity(violation_array)

            violation_keys = list(violation_embeddings.keys())
            for i in range(len(violation_keys)):
                for j in range(i+1, len(violation_keys)):
                    similarity = float(similarities[i, j])
                    if similarity >= threshold:
                        connections["violation_violation"].append({
                            "violation1": violation_keys[i],
                            "violation2": violation_keys[j],
                            "similarity": similarity,
                            "connection_type": "violation_violation"
                        })

        print(f"✅ Found connections:")
        print(f"   - Violation-Law: {len(connections['violation_law'])}")
        print(f"   - Violation-Form: {len(connections['violation_form'])}")
        print(f"   - Law-Form: {len(connections['law_form'])}")
        print(f"   - Violation-Violation: {len(connections['violation_violation'])}")

        self.connections = connections
        return connections

    def build_ground_truth_network(self, connections: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Build ground truth network graph of all connections"""
        print("\n🌐 Building ground truth network...")

        network = {
            "nodes": {
                "violations": {},
                "laws": {},
                "forms": {}
            },
            "edges": {
                "violation_law": [],
                "violation_form": [],
                "law_form": [],
                "violation_violation": []
            },
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_nodes": 0,
                "total_edges": 0
            }
        }

        # Add violation nodes
        violations_data = self.violations.get("violations", {})
        for category, items in violations_data.items():
            for item in items:
                node_id = f"violation_{category}_{item.get('entity_name', 'unknown')}"
                network["nodes"]["violations"][node_id] = {
                    "id": node_id,
                    "type": "violation",
                    "category": category,
                    "data": item
                }

        # Add law nodes (from ground truth embeddings)
        def extract_law_nodes(data, path=""):
            if isinstance(data, dict):
                if "ground_truth_embedding" in data:
                    node_id = f"law_{path}"
                    network["nodes"]["laws"][node_id] = {
                        "id": node_id,
                        "type": "law",
                        "name": data.get("name", ""),
                        "data": data
                    }
                for key, value in data.items():
                    if key not in ["ground_truth_embedding", "ground_truth_text"]:
                        extract_law_nodes(value, f"{path}.{key}" if path else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_law_nodes(item, f"{path}[{i}]")

        extract_law_nodes(self.laws)

        # Add form nodes
        def extract_form_nodes(data, path=""):
            if isinstance(data, dict):
                if "reporting_forms" in data:
                    for form in data["reporting_forms"]:
                        form_id = form.get("form_number") or form.get("form_name", "unknown")
                        node_id = f"form_{form_id}"
                        network["nodes"]["forms"][node_id] = {
                            "id": node_id,
                            "type": "form",
                            "data": form
                        }
                for key, value in data.items():
                    extract_form_nodes(value, f"{path}.{key}" if path else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_form_nodes(item, f"{path}[{i}]")

        extract_form_nodes(self.laws)

        # Add edges from connections
        for edge_type, edge_list in connections.items():
            network["edges"][edge_type] = edge_list

        # Calculate statistics
        network["metadata"]["total_nodes"] = (
            len(network["nodes"]["violations"]) +
            len(network["nodes"]["laws"]) +
            len(network["nodes"]["forms"])
        )
        network["metadata"]["total_edges"] = sum(len(edges) for edges in network["edges"].values())

        print(f"✅ Network built:")
        print(f"   - Nodes: {network['metadata']['total_nodes']}")
        print(f"   - Edges: {network['metadata']['total_edges']}")

        return network

    def cluster_connections(self, embeddings: Dict[str, np.ndarray],
                          eps: float = 0.5, min_samples: int = 2) -> Dict[str, Any]:
        """Cluster all embeddings to find patterns"""
        print(f"\n🔍 Clustering embeddings to find patterns...")

        # Combine all embeddings
        all_vectors = []
        all_ids = []
        for item_id, embedding in embeddings.items():
            all_vectors.append(embedding)
            all_ids.append(item_id)

        if len(all_vectors) < min_samples:
            print("   ⚠️  Not enough vectors to cluster")
            return {}

        all_vectors_array = np.array(all_vectors)

        # Use DBSCAN with parallel processing
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine', n_jobs=MAX_WORKERS)
        cluster_labels = clustering.fit_predict(all_vectors_array)

        # Organize clusters
        clusters = defaultdict(list)
        for i, label in enumerate(cluster_labels):
            if label != -1:
                clusters[f"cluster_{label}"].append({
                    "id": all_ids[i],
                    "embedding": all_vectors[i].tolist()
                })

        print(f"✅ Found {len(clusters)} clusters ({sum(1 for l in cluster_labels if l == -1)} noise points)")

        return {
            "clusters": dict(clusters),
            "n_clusters": len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0),
            "n_noise": sum(1 for l in cluster_labels if l == -1)
        }

    def generate_comprehensive_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive ML analysis with all connections"""
        print("\n📊 Generating comprehensive ML analysis...")

        # Extract all embeddings
        embeddings = self.extract_all_embeddings_parallel()

        # Find connections
        connections = self.find_connections_parallel(embeddings, threshold=0.7)

        # Build network
        network = self.build_ground_truth_network(connections)

        # Cluster
        clusters = self.cluster_connections(embeddings)

        analysis = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "model": "all-MiniLM-L6-v2",
                "dimension": 384,
                "parallel_workers": MAX_WORKERS,
                "batch_size": BATCH_SIZE
            },
            "summary": {
                "total_embeddings": len(embeddings),
                "total_connections": sum(len(c) for c in connections.values()),
                "network_nodes": network["metadata"]["total_nodes"],
                "network_edges": network["metadata"]["total_edges"],
                "clusters": clusters.get("n_clusters", 0)
            },
            "connections": connections,
            "network": network,
            "clusters": clusters,
            "embeddings_count": len(embeddings)
        }

        return analysis

    def save_results(self, output_file: Path):
        """Save comprehensive analysis results"""
        print(f"\n💾 Saving comprehensive analysis...")

        analysis = self.generate_comprehensive_analysis()

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved to {output_file}")
        print(f"   Total embeddings: {analysis['summary']['total_embeddings']}")
        print(f"   Total connections: {analysis['summary']['total_connections']}")
        print(f"   Network nodes: {analysis['summary']['network_nodes']}")
        print(f"   Network edges: {analysis['summary']['network_edges']}")


def main():
    """Main function to run advanced ML pipeline"""
    import time
    start_time = time.time()

    print("=" * 80)
    print("🚀 Advanced ML Pipeline - TensorFlow-Style Parallel Processing")
    print("=" * 80)
    print(f"Architecture: ARM M4 MAX")
    print(f"Workers: {MAX_WORKERS}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"RAM: 128GB")
    print("=" * 80)
    print()

    pipeline = AdvancedMLPipeline()

    # Load all data
    pipeline.load_all_data()

    # Generate comprehensive analysis
    analysis = pipeline.generate_comprehensive_analysis()

    # Save results
    output_file = DATA_PROCESSED_DIR / "advanced_ml_analysis.json"
    pipeline.save_results(output_file)

    total_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("✅ Advanced ML Pipeline Complete!")
    print("=" * 80)
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Embeddings: {analysis['summary']['total_embeddings']}")
    print(f"Connections: {analysis['summary']['total_connections']}")
    print(f"Network: {analysis['summary']['network_nodes']} nodes, {analysis['summary']['network_edges']} edges")
    print("=" * 80)


if __name__ == "__main__":
    main()
