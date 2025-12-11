#!/usr/bin/env python3
"""
Optimized Evidence-to-Law Matching with High-Performance Libraries
Uses FAISS for fast similarity search, optimized NumPy, and efficient batch processing
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import multiprocessing as mp

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR

# Optimize for ARM M4 MAX
MAX_WORKERS = os.cpu_count() or 16
BATCH_SIZE = 256  # Larger batches for better efficiency
print(f"🚀 Optimized Evidence-Law Matching - ARM M4 MAX ({MAX_WORKERS} workers)")

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    print("✅ FAISS available for fast similarity search")
except ImportError:
    print("Installing optimized libraries...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user",
                          "sentence-transformers", "faiss-cpu", "numpy", "scipy"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from sentence_transformers import SentenceTransformer
    import faiss
    print("✅ Optimized libraries installed")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine
    import scipy.spatial.distance as distance
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user",
                          "scikit-learn", "scipy"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine
    import scipy.spatial.distance as distance


class OptimizedEvidenceLawMatcher:
    """High-performance ML system using FAISS and optimized libraries"""
    
    def __init__(self):
        # Use faster model or optimize current one
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.violations = {}
        self.laws = {}
        self.forms = {}
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
        
        # FAISS index for fast similarity search
        self.faiss_index = None
        self.law_embeddings_array = None
        self.law_metadata = []
        
    def load_data(self):
        """Load violations, laws, and forms"""
        print("\n📂 Loading data...")
        
        violations_file = DATA_PROCESSED_DIR / "integrated_violations.json"
        if violations_file.exists():
            with open(violations_file, 'r', encoding='utf-8') as f:
                self.violations = json.load(f)
        
        law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
        if law_file.exists():
            with open(law_file, 'r', encoding='utf-8') as f:
                self.laws = json.load(f)
        
        self._extract_forms()
        
        violations_count = sum(len(v) for v in self.violations.get('violations', {}).values())
        print(f"   Loaded violations: {violations_count}")
        print(f"   Loaded laws")
        print(f"   Loaded forms: {len(self.forms)}")
    
    def _extract_forms(self):
        """Extract all reporting forms from laws"""
        def extract_forms_recursive(data, path=""):
            if isinstance(data, dict):
                if "reporting_forms" in data:
                    for form in data["reporting_forms"]:
                        form_id = form.get("form_number") or form.get("form_name", "unknown")
                        self.forms[form_id] = {
                            **form,
                            "law": data.get("name", ""),
                            "path": path
                        }
                for key, value in data.items():
                    if key not in ["embedding", "embedding_text", "ground_truth_embedding", "ground_truth_text"]:
                        extract_forms_recursive(value, f"{path}.{key}" if path else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_forms_recursive(item, f"{path}[{i}]")
        
        extract_forms_recursive(self.laws)
    
    def create_evidence_text(self, violation: Dict[str, Any]) -> str:
        """Create comprehensive evidence text"""
        parts = []
        parts.append(f"VIOLATION_TYPE: {violation.get('violation_type', '')}")
        parts.append(f"ENTITY: {violation.get('entity_name', '')}")
        parts.append(f"DESCRIPTION: {violation.get('description', '')}")
        parts.append(f"SEVERITY: {violation.get('severity', '')}")
        if violation.get('jurisdiction'):
            parts.append(f"JURISDICTION: {violation['jurisdiction']}")
        if violation.get('state'):
            parts.append(f"STATE: {violation['state']}")
        if violation.get('source'):
            parts.append(f"SOURCE: {violation['source']}")
        return " | ".join(parts)
    
    def build_faiss_index(self, law_embeddings: Dict[str, Dict]) -> None:
        """Build FAISS index for fast similarity search"""
        print("\n🔨 Building FAISS index for fast similarity search...")
        
        embeddings_list = []
        self.law_metadata = []
        
        for law_id, law_info in law_embeddings.items():
            embeddings_list.append(law_info["embedding"])
            self.law_metadata.append({
                "law_id": law_id,
                "law_info": law_info
            })
        
        # Convert to numpy array
        self.law_embeddings_array = np.array(embeddings_list, dtype=np.float32)
        dimension = self.law_embeddings_array.shape[1]
        
        # Create FAISS index (Inner Product for cosine similarity on normalized vectors)
        # Using IndexFlatIP (Inner Product) since embeddings are normalized
        self.faiss_index = faiss.IndexFlatIP(dimension)
        
        # Add vectors to index
        self.faiss_index.add(self.law_embeddings_array)
        
        print(f"   ✅ FAISS index built: {self.faiss_index.ntotal} vectors, dimension {dimension}")
    
    def fast_similarity_search(self, evidence_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[int, float]]:
        """Fast similarity search using FAISS"""
        # Ensure evidence embedding is normalized and float32
        evidence_embedding = evidence_embedding.astype(np.float32)
        evidence_embedding = evidence_embedding / np.linalg.norm(evidence_embedding)
        evidence_embedding = evidence_embedding.reshape(1, -1)
        
        # Search using FAISS (much faster than sklearn)
        distances, indices = self.faiss_index.search(evidence_embedding, top_k)
        
        # Return (index, similarity_score) pairs
        # FAISS returns inner product (which is cosine similarity for normalized vectors)
        results = [(int(idx), float(dist)) for idx, dist in zip(indices[0], distances[0])]
        return results
    
    def compute_optimized_similarities(self, evidence_embedding: np.ndarray,
                                      law_embedding: np.ndarray) -> Dict[str, float]:
        """Compute similarities using optimized NumPy operations"""
        similarities = {}
        
        # Normalize once
        evidence_norm = evidence_embedding / np.linalg.norm(evidence_embedding)
        law_norm = law_embedding / np.linalg.norm(law_embedding)
        
        # 1. Cosine Similarity (using dot product on normalized vectors - fastest)
        similarities["cosine"] = float(np.dot(evidence_norm, law_norm))
        
        # 2. Euclidean Distance (vectorized)
        euclidean_dist = np.linalg.norm(evidence_embedding - law_embedding)
        similarities["euclidean"] = float(1 / (1 + euclidean_dist))
        
        # 3. Manhattan Distance (vectorized)
        manhattan_dist = np.sum(np.abs(evidence_embedding - law_embedding))
        similarities["manhattan"] = float(1 / (1 + manhattan_dist))
        
        # 4. Dot Product
        similarities["dot_product"] = float(np.dot(evidence_embedding, law_embedding))
        
        # 5. Jaccard Similarity (vectorized binary operations)
        evidence_binary = (evidence_embedding > 0).astype(np.uint8)
        law_binary = (law_embedding > 0).astype(np.uint8)
        intersection = np.sum(evidence_binary & law_binary)
        union = np.sum(evidence_binary | law_binary)
        similarities["jaccard"] = float(intersection / union) if union > 0 else 0.0
        
        # 6. Pearson Correlation (vectorized)
        if len(evidence_embedding) > 1:
            correlation = np.corrcoef(evidence_embedding, law_embedding)[0, 1]
            similarities["pearson"] = float(correlation) if not np.isnan(correlation) else 0.0
        else:
            similarities["pearson"] = 0.0
        
        return similarities
    
    def batch_compute_tfidf(self, evidence_texts: List[str], law_texts: List[str]) -> np.ndarray:
        """Batch compute TF-IDF similarities (much faster than individual)"""
        try:
            all_texts = evidence_texts + law_texts
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_texts)
            
            # Split into evidence and law matrices
            evidence_tfidf = tfidf_matrix[:len(evidence_texts)]
            law_tfidf = tfidf_matrix[len(evidence_texts):]
            
            # Batch cosine similarity
            similarities = sklearn_cosine(evidence_tfidf, law_tfidf)
            return similarities
        except:
            return np.zeros((len(evidence_texts), len(law_texts)))
    
    def compute_form_weight(self, violation: Dict[str, Any], law_data: Dict[str, Any]) -> float:
        """Compute form-based weight"""
        forms = law_data.get("reporting_forms", [])
        if not forms:
            return 0.5
        
        violation_type = violation.get("violation_type", "").lower()
        jurisdiction = violation.get("jurisdiction", "").lower()
        severity = violation.get("severity", "").upper()
        
        weight = 0.5
        weight += min(0.2, len(forms) * 0.05)
        
        for form in forms:
            form_desc = form.get("description", "").lower()
            form_name = form.get("form_name", "").lower()
            
            if any(term in form_desc or term in form_name for term in violation_type.split()):
                weight += 0.1
            
            form_agency = form.get("agency", "").lower()
            if jurisdiction in form_agency or form_agency in jurisdiction:
                weight += 0.1
        
        if severity == "HIGH":
            weight += 0.1
        elif severity == "MEDIUM":
            weight += 0.05
        
        return min(1.0, weight)
    
    def optimized_match(self, evidence_text: str, evidence_embedding: np.ndarray,
                       top_k: int = 5) -> List[Dict[str, Any]]:
        """Optimized matching using FAISS and batch operations"""
        matches = []
        
        # Fast FAISS search
        faiss_results = self.fast_similarity_search(evidence_embedding, top_k * 2)  # Get more for filtering
        
        # Extract violation info for form weighting
        violation_dict = {
            "violation_type": evidence_text.split("VIOLATION_TYPE:")[1].split("|")[0].strip() if "VIOLATION_TYPE:" in evidence_text else "",
            "jurisdiction": evidence_text.split("JURISDICTION:")[1].split("|")[0].strip() if "JURISDICTION:" in evidence_text else "",
            "severity": evidence_text.split("SEVERITY:")[1].split("|")[0].strip() if "SEVERITY:" in evidence_text else "MEDIUM"
        }
        
        for idx, faiss_score in faiss_results:
            if idx >= len(self.law_metadata):
                continue
                
            law_meta = self.law_metadata[idx]
            law_info = law_meta["law_info"]
            law_embedding = law_info["embedding"]
            law_text = law_info["text"]
            law_data = law_info["law_data"]
            
            # Compute additional similarities (only for top candidates)
            similarities = self.compute_optimized_similarities(evidence_embedding, law_embedding)
            similarities["faiss_cosine"] = faiss_score  # FAISS result
            
            # TF-IDF (compute on-demand for top candidates)
            try:
                tfidf_sim = self.compute_tfidf_similarity(evidence_text, law_text)
                similarities["tfidf"] = tfidf_sim
            except:
                similarities["tfidf"] = 0.0
            
            # Form weight
            form_weight = self.compute_form_weight(violation_dict, law_data)
            
            # Ensemble score
            ensemble_score = (
                0.25 * similarities["cosine"] +  # Use FAISS result
                0.15 * similarities["euclidean"] +
                0.10 * similarities["manhattan"] +
                0.10 * similarities["dot_product"] +
                0.10 * similarities["jaccard"] +
                0.10 * similarities["pearson"] +
                0.10 * similarities["tfidf"] +
                0.10 * form_weight
            )
            
            if law_info.get("is_ground_truth"):
                ensemble_score *= 1.1
            
            matches.append({
                "law_id": law_meta["law_id"],
                "law_name": law_data.get("name", ""),
                "ensemble_score": ensemble_score,
                "similarities": similarities,
                "form_weight": form_weight,
                "is_ground_truth": law_info.get("is_ground_truth", False),
                "law_data": law_data
            })
        
        matches.sort(key=lambda x: x["ensemble_score"], reverse=True)
        return matches[:top_k]
    
    def compute_tfidf_similarity(self, evidence_text: str, law_text: str) -> float:
        """Compute TF-IDF similarity"""
        try:
            texts = [evidence_text, law_text]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            similarity = sklearn_cosine(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def match_all_evidence_optimized(self, top_k: int = 5) -> Dict[str, Any]:
        """Optimized batch matching using FAISS"""
        print("\n🔗 Fast matching evidence to laws using FAISS and optimized operations...")
        
        # Extract law embeddings
        law_embeddings = {}
        def extract_laws_recursive(data, path=""):
            if isinstance(data, dict):
                if "ground_truth_embedding" in data and "ground_truth_text" in data:
                    law_id = f"law_{path}"
                    law_embeddings[law_id] = {
                        "embedding": np.array(data["ground_truth_embedding"], dtype=np.float32),
                        "text": data["ground_truth_text"],
                        "law_data": data,
                        "is_ground_truth": True
                    }
                elif "embedding" in data and "embedding_text" in data:
                    law_id = f"law_{path}"
                    law_embeddings[law_id] = {
                        "embedding": np.array(data["embedding"], dtype=np.float32),
                        "text": data["embedding_text"],
                        "law_data": data,
                        "is_ground_truth": False
                    }
                for key, value in data.items():
                    if key not in ["embedding", "embedding_text", "ground_truth_embedding", "ground_truth_text"]:
                        extract_laws_recursive(value, f"{path}.{key}" if path else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_laws_recursive(item, f"{path}[{i}]")
        
        extract_laws_recursive(self.laws)
        print(f"   Extracted {len(law_embeddings)} law embeddings")
        
        # Build FAISS index
        self.build_faiss_index(law_embeddings)
        
        # Collect evidence
        violations_data = self.violations.get("violations", {})
        evidence_list = []
        
        print(f"   Encoding evidence in batches of {BATCH_SIZE}...")
        for category, items in violations_data.items():
            for item in items:
                evidence_text = self.create_evidence_text(item)
                evidence_list.append({
                    "violation": item,
                    "category": category,
                    "text": evidence_text
                })
        
        # Batch encode all evidence at once (much faster)
        evidence_texts = [e["text"] for e in evidence_list]
        evidence_embeddings = self.model.encode(
            evidence_texts,
            normalize_embeddings=True,
            batch_size=BATCH_SIZE,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        
        print(f"   Processing {len(evidence_list)} evidence items with FAISS...")
        
        # Process in parallel batches
        def process_batch(batch_indices):
            batch_matches = []
            for idx in batch_indices:
                evidence = evidence_list[idx]
                evidence_embedding = evidence_embeddings[idx]
                matches = self.optimized_match(evidence["text"], evidence_embedding, top_k)
                batch_matches.append({
                    "violation": evidence["violation"],
                    "category": evidence["category"],
                    "matches": matches
                })
            return batch_matches
        
        # Parallel processing
        batch_size = max(1, len(evidence_list) // MAX_WORKERS)
        batches = [list(range(i, min(i+batch_size, len(evidence_list)))) 
                  for i in range(0, len(evidence_list), batch_size)]
        
        all_matches = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(process_batch, batch) for batch in batches]
            for future in as_completed(futures):
                try:
                    batch_matches = future.result()
                    all_matches.extend(batch_matches)
                except Exception as e:
                    print(f"   ⚠️  Error in batch: {e}")
        
        print(f"✅ Matched {len(all_matches)} evidence items to laws")
        
        return {
            "matched_evidence": all_matches,
            "total_evidence": len(evidence_list),
            "total_laws": len(law_embeddings),
            "techniques_used": [
                "faiss_fast_similarity_search",
                "optimized_cosine_similarity",
                "vectorized_euclidean_distance",
                "vectorized_manhattan_distance",
                "vectorized_dot_product",
                "vectorized_jaccard_similarity",
                "vectorized_pearson_correlation",
                "batch_tfidf_similarity",
                "form_based_weighting",
                "ground_truth_bonus",
                "ensemble_scoring"
            ]
        }
    
    def generate_report(self, matches: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive report"""
        print("\n📊 Generating report...")
        
        all_scores = [
            m["ensemble_score"]
            for evidence in matches["matched_evidence"]
            for m in evidence["matches"]
        ]
        
        avg_score = np.mean(all_scores) if all_scores else 0.0
        
        form_weighted = sum(1 for e in matches["matched_evidence"]
                           for m in e["matches"] if m.get("form_weight", 0) > 0.6)
        
        ground_truth = sum(1 for e in matches["matched_evidence"]
                          for m in e["matches"] if m.get("is_ground_truth", False))
        
        report = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "model": "all-MiniLM-L6-v2",
                "techniques": matches["techniques_used"],
                "parallel_workers": MAX_WORKERS,
                "batch_size": BATCH_SIZE,
                "optimization": "FAISS + Optimized NumPy + Batch Processing"
            },
            "statistics": {
                "total_evidence": matches["total_evidence"],
                "total_laws": matches["total_laws"],
                "total_matches": sum(len(m["matches"]) for m in matches["matched_evidence"]),
                "average_ensemble_score": float(avg_score),
                "form_weighted_matches": form_weighted,
                "ground_truth_matches": ground_truth
            },
            "matches": matches["matched_evidence"]
        }
        
        return report


def main():
    """Main function"""
    import time
    start_time = time.time()
    
    print("=" * 80)
    print("⚡ Optimized Evidence-Law Matching - High-Performance Libraries")
    print("=" * 80)
    print(f"Architecture: ARM M4 MAX")
    print(f"Workers: {MAX_WORKERS}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Libraries: FAISS, Optimized NumPy, Batch Processing")
    print("=" * 80)
    print()
    
    matcher = OptimizedEvidenceLawMatcher()
    matcher.load_data()
    
    matches = matcher.match_all_evidence_optimized(top_k=5)
    
    report = matcher.generate_report(matches)
    
    output_file = DATA_PROCESSED_DIR / "optimized_evidence_law_matching.json"
    print(f"\n💾 Saving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    total_time = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("✅ Optimized Evidence-Law Matching Complete!")
    print("=" * 80)
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Evidence items: {report['statistics']['total_evidence']}")
    print(f"Laws matched: {report['statistics']['total_laws']}")
    print(f"Total matches: {report['statistics']['total_matches']}")
    print(f"Average ensemble score: {report['statistics']['average_ensemble_score']:.4f}")
    print(f"Form-weighted matches: {report['statistics']['form_weighted_matches']}")
    print(f"Ground truth matches: {report['statistics']['ground_truth_matches']}")
    print(f"Throughput: {report['statistics']['total_evidence']/total_time:.1f} items/second")
    print("=" * 80)


if __name__ == "__main__":
    main()
