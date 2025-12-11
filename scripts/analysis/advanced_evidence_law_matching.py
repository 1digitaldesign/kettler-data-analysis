#!/usr/bin/env python3
"""
Advanced Evidence-to-Law Matching with Multiple AI/ML Techniques
Uses ensemble methods, multiple similarity metrics, and form-based weighting
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

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, DATA_VECTORS_DIR

# Optimize for ARM M4 MAX
MAX_WORKERS = os.cpu_count() or 16
BATCH_SIZE = 128
print(f"🚀 Advanced Evidence-Law Matching - ARM M4 MAX Optimized ({MAX_WORKERS} workers)")

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import PCA, LatentSemanticAnalysis
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler
    import scipy.spatial.distance as distance
    print("✅ All ML libraries available")
except ImportError:
    print("Installing ML libraries...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user",
                          "sentence-transformers", "scikit-learn", "numpy", "scipy"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import PCA
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler
    import scipy.spatial.distance as distance
    print("✅ ML libraries installed")


class AdvancedEvidenceLawMatcher:
    """Advanced ML system for matching evidence to ground truth laws with form-based weighting"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.violations = {}
        self.laws = {}
        self.forms = {}
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
        self.scaler = StandardScaler()
        
    def load_data(self):
        """Load violations, laws, and forms"""
        print("\n📂 Loading data...")
        
        # Load violations
        violations_file = DATA_PROCESSED_DIR / "integrated_violations.json"
        if violations_file.exists():
            with open(violations_file, 'r', encoding='utf-8') as f:
                self.violations = json.load(f)
        
        # Load laws
        law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
        if law_file.exists():
            with open(law_file, 'r', encoding='utf-8') as f:
                self.laws = json.load(f)
        
        # Extract forms from laws
        self._extract_forms()
        
        print(f"   Loaded violations: {sum(len(v) for v in self.violations.get('violations', {}).values())}")
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
        """Create comprehensive evidence text for matching"""
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
    
    def extract_law_embeddings(self) -> Dict[str, np.ndarray]:
        """Extract all law embeddings (prioritize ground truth)"""
        print("\n🔍 Extracting law embeddings...")
        
        law_embeddings = {}
        law_texts = []
        law_ids = []
        
        def extract_laws_recursive(data, path=""):
            if isinstance(data, dict):
                # Prioritize ground truth embeddings
                if "ground_truth_embedding" in data and "ground_truth_text" in data:
                    law_id = f"law_{path}"
                    law_embeddings[law_id] = {
                        "embedding": np.array(data["ground_truth_embedding"]),
                        "text": data["ground_truth_text"],
                        "law_data": data,
                        "is_ground_truth": True
                    }
                    law_texts.append(data["ground_truth_text"])
                    law_ids.append(law_id)
                elif "embedding" in data and "embedding_text" in data:
                    law_id = f"law_{path}"
                    law_embeddings[law_id] = {
                        "embedding": np.array(data["embedding"]),
                        "text": data["embedding_text"],
                        "law_data": data,
                        "is_ground_truth": False
                    }
                    law_texts.append(data["embedding_text"])
                    law_ids.append(law_id)
                
                for key, value in data.items():
                    if key not in ["embedding", "embedding_text", "ground_truth_embedding", "ground_truth_text"]:
                        extract_laws_recursive(value, f"{path}.{key}" if path else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_laws_recursive(item, f"{path}[{i}]")
        
        extract_laws_recursive(self.laws)
        
        print(f"   Extracted {len(law_embeddings)} law embeddings")
        return law_embeddings
    
    def compute_multiple_similarities(self, evidence_embedding: np.ndarray, 
                                     law_embedding: np.ndarray) -> Dict[str, float]:
        """Compute multiple similarity metrics"""
        similarities = {}
        
        # 1. Cosine Similarity (default)
        similarities["cosine"] = float(1 - distance.cosine(evidence_embedding, law_embedding))
        
        # 2. Euclidean Distance (inverted to similarity)
        euclidean_dist = np.linalg.norm(evidence_embedding - law_embedding)
        similarities["euclidean"] = float(1 / (1 + euclidean_dist))
        
        # 3. Manhattan Distance (inverted)
        manhattan_dist = np.sum(np.abs(evidence_embedding - law_embedding))
        similarities["manhattan"] = float(1 / (1 + manhattan_dist))
        
        # 4. Dot Product (normalized)
        dot_product = np.dot(evidence_embedding, law_embedding)
        similarities["dot_product"] = float(dot_product)
        
        # 5. Jaccard Similarity (on binarized vectors)
        evidence_binary = (evidence_embedding > 0).astype(int)
        law_binary = (law_embedding > 0).astype(int)
        intersection = np.sum(evidence_binary & law_binary)
        union = np.sum(evidence_binary | law_binary)
        similarities["jaccard"] = float(intersection / union) if union > 0 else 0.0
        
        # 6. Pearson Correlation
        if len(evidence_embedding) > 1:
            correlation = np.corrcoef(evidence_embedding, law_embedding)[0, 1]
            similarities["pearson"] = float(correlation) if not np.isnan(correlation) else 0.0
        else:
            similarities["pearson"] = 0.0
        
        return similarities
    
    def compute_tfidf_similarity(self, evidence_text: str, law_text: str) -> float:
        """Compute TF-IDF similarity"""
        try:
            # Fit and transform
            texts = [evidence_text, law_text]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def compute_form_weight(self, violation: Dict[str, Any], law_data: Dict[str, Any]) -> float:
        """Compute weight based on available reporting forms"""
        # Check if law has reporting forms
        forms = law_data.get("reporting_forms", [])
        if not forms:
            return 0.5  # Default weight if no forms
        
        # Extract violation characteristics
        violation_type = violation.get("violation_type", "").lower()
        jurisdiction = violation.get("jurisdiction", "").lower()
        severity = violation.get("severity", "").upper()
        
        # Weight factors
        weight = 0.5  # Base weight
        
        # More forms = higher weight
        weight += min(0.2, len(forms) * 0.05)
        
        # Check form relevance to violation
        for form in forms:
            form_desc = form.get("description", "").lower()
            form_name = form.get("form_name", "").lower()
            
            # Check if form matches violation type
            if any(term in form_desc or term in form_name for term in violation_type.split()):
                weight += 0.1
            
            # Check jurisdiction match
            form_agency = form.get("agency", "").lower()
            if jurisdiction in form_agency or form_agency in jurisdiction:
                weight += 0.1
        
        # Higher severity = higher weight
        if severity == "HIGH":
            weight += 0.1
        elif severity == "MEDIUM":
            weight += 0.05
        
        return min(1.0, weight)
    
    def ensemble_match(self, evidence_text: str, evidence_embedding: np.ndarray,
                      law_embeddings: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Use ensemble of ML techniques to match evidence to laws"""
        matches = []
        
        for law_id, law_info in law_embeddings.items():
            law_embedding = law_info["embedding"]
            law_text = law_info["text"]
            law_data = law_info["law_data"]
            
            # Compute multiple similarity metrics
            similarities = self.compute_multiple_similarities(evidence_embedding, law_embedding)
            
            # TF-IDF similarity
            tfidf_sim = self.compute_tfidf_similarity(evidence_text, law_text)
            similarities["tfidf"] = tfidf_sim
            
            # Form-based weight
            # Create a dummy violation dict for form weight calculation
            violation_dict = {
                "violation_type": evidence_text.split("VIOLATION_TYPE:")[1].split("|")[0].strip() if "VIOLATION_TYPE:" in evidence_text else "",
                "jurisdiction": evidence_text.split("JURISDICTION:")[1].split("|")[0].strip() if "JURISDICTION:" in evidence_text else "",
                "severity": evidence_text.split("SEVERITY:")[1].split("|")[0].strip() if "SEVERITY:" in evidence_text else "MEDIUM"
            }
            form_weight = self.compute_form_weight(violation_dict, law_data)
            
            # Ensemble score (weighted combination)
            ensemble_score = (
                0.30 * similarities["cosine"] +  # Primary metric
                0.15 * similarities["euclidean"] +
                0.10 * similarities["manhattan"] +
                0.10 * similarities["dot_product"] +
                0.10 * similarities["jaccard"] +
                0.10 * similarities["pearson"] +
                0.10 * similarities["tfidf"] +
                0.05 * form_weight  # Form-based weight
            )
            
            # Ground truth bonus
            if law_info.get("is_ground_truth"):
                ensemble_score *= 1.1  # 10% bonus for ground truth
            
            matches.append({
                "law_id": law_id,
                "law_name": law_data.get("name", ""),
                "ensemble_score": ensemble_score,
                "similarities": similarities,
                "form_weight": form_weight,
                "is_ground_truth": law_info.get("is_ground_truth", False),
                "law_data": law_data
            })
        
        # Sort by ensemble score
        matches.sort(key=lambda x: x["ensemble_score"], reverse=True)
        return matches
    
    def match_all_evidence(self, top_k: int = 5) -> Dict[str, Any]:
        """Match all evidence to laws using advanced ML techniques"""
        print("\n🔗 Matching evidence to laws using ensemble ML techniques...")
        
        # Extract law embeddings
        law_embeddings = self.extract_law_embeddings()
        
        # Process violations
        violations_data = self.violations.get("violations", {})
        all_matches = []
        
        # Collect all evidence
        evidence_list = []
        for category, items in violations_data.items():
            for item in items:
                evidence_text = self.create_evidence_text(item)
                evidence_embedding = self.model.encode(evidence_text, normalize_embeddings=True)
                evidence_list.append({
                    "violation": item,
                    "category": category,
                    "text": evidence_text,
                    "embedding": evidence_embedding
                })
        
        print(f"   Processing {len(evidence_list)} evidence items...")
        
        # Process in parallel batches
        def process_evidence_batch(batch):
            batch_matches = []
            for evidence in batch:
                matches = self.ensemble_match(
                    evidence["text"],
                    evidence["embedding"],
                    law_embeddings
                )
                # Get top K matches
                top_matches = matches[:top_k]
                batch_matches.append({
                    "violation": evidence["violation"],
                    "category": evidence["category"],
                    "matches": top_matches
                })
            return batch_matches
        
        # Process in parallel
        batch_size = max(1, len(evidence_list) // MAX_WORKERS)
        batches = [evidence_list[i:i+batch_size] for i in range(0, len(evidence_list), batch_size)]
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(process_evidence_batch, batch) for batch in batches]
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
                "cosine_similarity",
                "euclidean_distance",
                "manhattan_distance",
                "dot_product",
                "jaccard_similarity",
                "pearson_correlation",
                "tfidf_similarity",
                "form_based_weighting",
                "ground_truth_bonus",
                "ensemble_scoring"
            ]
        }
    
    def generate_ml_analysis_report(self, matches: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive ML analysis report"""
        print("\n📊 Generating ML analysis report...")
        
        # Statistics
        total_matches = sum(len(m["matches"]) for m in matches["matched_evidence"])
        avg_score = np.mean([
            m["ensemble_score"]
            for evidence in matches["matched_evidence"]
            for m in evidence["matches"]
        ])
        
        # Form-weighted matches
        form_weighted_matches = [
            m for evidence in matches["matched_evidence"]
            for m in evidence["matches"]
            if m["form_weight"] > 0.6
        ]
        
        # Ground truth matches
        ground_truth_matches = [
            m for evidence in matches["matched_evidence"]
            for m in evidence["matches"]
            if m["is_ground_truth"]
        ]
        
        report = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "model": "all-MiniLM-L6-v2",
                "techniques": matches["techniques_used"],
                "parallel_workers": MAX_WORKERS,
                "batch_size": BATCH_SIZE
            },
            "statistics": {
                "total_evidence": matches["total_evidence"],
                "total_laws": matches["total_laws"],
                "total_matches": total_matches,
                "average_ensemble_score": float(avg_score),
                "form_weighted_matches": len(form_weighted_matches),
                "ground_truth_matches": len(ground_truth_matches)
            },
            "matches": matches["matched_evidence"]
        }
        
        return report


def main():
    """Main function"""
    import time
    start_time = time.time()
    
    print("=" * 80)
    print("🤖 Advanced Evidence-Law Matching with Multiple AI/ML Techniques")
    print("=" * 80)
    print(f"Architecture: ARM M4 MAX")
    print(f"Workers: {MAX_WORKERS}")
    print(f"Batch Size: {BATCH_SIZE}")
    print("=" * 80)
    print()
    
    matcher = AdvancedEvidenceLawMatcher()
    matcher.load_data()
    
    # Match all evidence
    matches = matcher.match_all_evidence(top_k=5)
    
    # Generate report
    report = matcher.generate_ml_analysis_report(matches)
    
    # Save results
    output_file = DATA_PROCESSED_DIR / "advanced_evidence_law_matching.json"
    print(f"\n💾 Saving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    total_time = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("✅ Advanced Evidence-Law Matching Complete!")
    print("=" * 80)
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Evidence items: {report['statistics']['total_evidence']}")
    print(f"Laws matched: {report['statistics']['total_laws']}")
    print(f"Total matches: {report['statistics']['total_matches']}")
    print(f"Average ensemble score: {report['statistics']['average_ensemble_score']:.4f}")
    print(f"Form-weighted matches: {report['statistics']['form_weighted_matches']}")
    print(f"Ground truth matches: {report['statistics']['ground_truth_matches']}")
    print(f"Techniques used: {len(report['metadata']['techniques'])}")
    print("=" * 80)


if __name__ == "__main__":
    main()
