#!/usr/bin/env python3
"""
Discover and Curate New Violations Dataset
Analyzes all data sources to find new violations not yet in the dataset
Uses ML and pattern matching to identify potential violations
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict
import re
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import multiprocessing as mp

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, DATA_VECTORS_DIR, DATA_RAW_DIR, RESEARCH_DIR

# Optimize for ARM M4 MAX - use all cores and leverage 128GB RAM
MAX_WORKERS = os.cpu_count() or 16
print(f"🚀 Optimized for ARM M4 MAX: Using {MAX_WORKERS} parallel workers, 128GB RAM available")

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user",
                          "sentence-transformers", "scikit-learn", "numpy"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity


class ViolationDiscoverySystem:
    """System for discovering new violations from various data sources"""

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.existing_violations = set()
        self.discovered_violations = []
        self.violation_patterns = self._load_violation_patterns()

    def _load_violation_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for detecting violations"""
        return {
            "tax_violations": [
                "tax forfeiture", "tax evasion", "failure to pay tax", "tax fraud",
                "delinquent tax", "tax penalty", "tax lien", "tax delinquency"
            ],
            "licensing_violations": [
                "unlicensed", "license required", "license violation", "no license",
                "license expired", "license suspended", "license revoked", "operating without license"
            ],
            "filing_violations": [
                "late filing", "failure to file", "overdue filing", "delinquent filing",
                "filing violation", "missed filing", "filing deadline"
            ],
            "entity_violations": [
                "forfeited existence", "forfeited entity", "entity forfeiture",
                "dissolved entity", "inactive entity", "entity status violation"
            ],
            "regulatory_violations": [
                "regulatory violation", "compliance violation", "regulatory non-compliance",
                "violation of", "breach of", "non-compliance with"
            ],
            "fraud_violations": [
                "fraud", "false statement", "misrepresentation", "deceptive practice",
                "fraudulent", "scheme to defraud", "wire fraud", "mail fraud"
            ],
            "property_violations": [
                "property violation", "landlord violation", "tenant violation",
                "housing violation", "property code violation", "unsafe property"
            ]
        }

    def load_existing_violations(self, violations_file: Path) -> Set[str]:
        """Load existing violations to avoid duplicates"""
        print(f"Loading existing violations from {violations_file}...")
        existing = set()

        try:
            with open(violations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            violations = data.get("violations", {})
            for category, items in violations.items():
                for item in items:
                    # Create unique identifier
                    entity = item.get("entity_name", "")
                    violation_type = item.get("violation_type", "")
                    date = item.get("filing_date") or item.get("effective_date", "")
                    key = f"{entity}_{violation_type}_{date}"
                    existing.add(key.lower())

            print(f"✅ Loaded {len(existing)} existing violations")
            self.existing_violations = existing
            return existing
        except Exception as e:
            print(f"⚠️  Error loading existing violations: {e}")
            return set()

    def discover_from_lariat_data(self, lariat_file: Path) -> List[Dict[str, Any]]:
        """Discover violations from Lariat TX data"""
        print(f"\n🔍 Discovering violations from Lariat data...")
        violations = []

        try:
            with open(lariat_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for tax forfeitures
            if "Tax Forfeiture" in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "Tax Forfeiture" in line:
                        # Extract entity and date information
                        entity_match = re.search(r'Name:\s*([^\n|]+)', content[max(0, i-20):i+20])
                        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content[max(0, i-20):i+20])
                        filing_match = re.search(r'Filing Number:\s*(\d+)', content[max(0, i-20):i+20])

                        if entity_match:
                            entity = entity_match.group(1).strip()
                            key = f"{entity}_tax_forfeiture_{date_match.group(1) if date_match else ''}"

                            if key.lower() not in self.existing_violations:
                                violations.append({
                                    "violation_type": "Tax Forfeiture",
                                    "entity_name": entity,
                                    "filing_number": filing_match.group(1) if filing_match else None,
                                    "date": date_match.group(1) if date_match else None,
                                    "source": "lariat_tx_data",
                                    "severity": "HIGH",
                                    "description": f"Tax forfeiture found in Lariat data for {entity}"
                                })

            # Look for forfeited entities
            if "Forfeited" in content or "forfeited existence" in content.lower():
                # Similar pattern matching for forfeited entities
                pass

            print(f"   Found {len(violations)} new violations in Lariat data")
            return violations

        except Exception as e:
            print(f"⚠️  Error processing Lariat data: {e}")
            return []

    def _process_single_report(self, md_file: Path, research_dir: Path) -> List[Dict[str, Any]]:
        """Process a single report file (for parallel execution)"""
        violations = []
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract violations using pattern matching with better entity extraction
            lines = content.split('\n')
            for i, line in enumerate(lines):
                for violation_type, patterns in self.violation_patterns.items():
                    for pattern in patterns:
                        if pattern.lower() in line.lower():
                            # Better entity name extraction
                            entity = None

                            # Pattern 1: "Name - Violation" format
                            entity_match = re.search(r'^###?\s*\d+\.\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\s*-', line)
                            if entity_match:
                                entity = entity_match.group(1).strip()

                            # Pattern 2: Look in previous lines
                            if not entity:
                                for j in range(max(0, i-3), i):
                                    entity_match = re.search(r'([A-Z][a-z]+\s+[A-Z][a-z]+)', lines[j])
                                    if entity_match:
                                        potential = entity_match.group(1).strip()
                                        if potential not in ["Date December", "Status CONFIRMED", "Severity HIGH"]:
                                            entity = potential
                                            break

                            # Pattern 3: Company names
                            if not entity:
                                company_match = re.search(r'([A-Z][A-Za-z\s&,]+(?:Inc|LLC|Corp|Ltd)\.?)', line)
                                if company_match:
                                    entity = company_match.group(1).strip()

                            if entity and len(entity.split()) <= 4:
                                key = f"{entity}_{violation_type}_{md_file.stem}"
                                if key.lower() not in self.existing_violations:
                                    violations.append({
                                        "violation_type": violation_type.replace("_", " ").title(),
                                        "entity_name": entity,
                                        "source": str(md_file.relative_to(research_dir)),
                                        "severity": "HIGH" if "unlicensed" in pattern.lower() or "fraud" in pattern.lower() else "MEDIUM",
                                        "description": f"Violation found in {md_file.name}: {line.strip()[:200]}",
                                        "line_context": line.strip()
                                    })
                            break
        except Exception as e:
            pass  # Silently skip errors in parallel processing
        return violations

    def discover_from_research_reports(self, research_dir: Path) -> List[Dict[str, Any]]:
        """Discover violations from research reports (parallel processing)"""
        print(f"\n🔍 Discovering violations from research reports (parallel)...")
        violations = []

        reports_dir = research_dir / "reports"
        if not reports_dir.exists():
            return violations

        # Collect all report files
        report_files = list(reports_dir.glob("*VIOLATION*.md"))
        print(f"   Processing {len(report_files)} report files in parallel...")

        # Process files in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_file = {executor.submit(self._process_single_report, md_file, research_dir): md_file
                             for md_file in report_files}

            completed = 0
            for future in as_completed(future_to_file):
                try:
                    file_violations = future.result()
                    violations.extend(file_violations)
                    completed += 1
                    if completed % 5 == 0 or completed == len(report_files):
                        print(f"   Progress: {completed}/{len(report_files)} files processed")
                except Exception as e:
                    md_file = future_to_file[future]
                    print(f"   ⚠️  Error processing {md_file.name}: {e}")

        print(f"   Found {len(violations)} new violations in research reports")
        return violations

    def _process_license_file(self, json_file: Path, state_name: str, research_dir: Path) -> Optional[Dict[str, Any]]:
        """Process a single license search file (for parallel execution)"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check for "no license found" or similar indicators
            data_str = json.dumps(data).lower()
            if any(term in data_str for term in ["no license", "not found", "no record", "unlicensed"]):
                # Extract person/entity name from filename
                name_match = re.search(r'([a-z_]+)_finding', json_file.stem)
                if name_match:
                    person_name = name_match.group(1).replace('_', ' ').title()
                    key = f"{person_name}_licensing_violation_{state_name}"

                    if key.lower() not in self.existing_violations:
                        return {
                            "violation_type": "Unlicensed Practice",
                            "entity_name": person_name,
                            "state": state_name,
                            "source": str(json_file.relative_to(research_dir)),
                            "severity": "HIGH",
                            "description": f"No license found for {person_name} in {state_name}"
                        }
        except Exception:
            pass
        return None

    def discover_from_license_searches(self, research_dir: Path) -> List[Dict[str, Any]]:
        """Discover licensing violations from license search results (parallel processing)"""
        print(f"\n🔍 Discovering violations from license searches (parallel)...")
        violations = []

        license_dir = research_dir / "license_searches" / "data"
        if not license_dir.exists():
            return violations

        # Collect all JSON files
        json_files = []
        for state_dir in license_dir.iterdir():
            if state_dir.is_dir():
                state_name = state_dir.name
                for json_file in state_dir.glob("*.json"):
                    json_files.append((json_file, state_name))

        print(f"   Processing {len(json_files)} license files in parallel...")

        # Process files in parallel
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_file = {executor.submit(self._process_license_file, json_file, state_name, research_dir): json_file
                             for json_file, state_name in json_files}

            completed = 0
            for future in as_completed(future_to_file):
                try:
                    violation = future.result()
                    if violation:
                        violations.append(violation)
                    completed += 1
                    if completed % 50 == 0 or completed == len(json_files):
                        print(f"   Progress: {completed}/{len(json_files)} files processed")
                except Exception:
                    pass

        print(f"   Found {len(violations)} new violations in license searches")
        return violations

    def discover_from_dpor_data(self, dpor_file: Path) -> List[Dict[str, Any]]:
        """Discover violations from DPOR complaint data"""
        print(f"\n🔍 Discovering violations from DPOR data...")
        violations = []

        if not dpor_file.exists():
            print(f"   ⚠️  DPOR file not found: {dpor_file}")
            return violations

        try:
            with open(dpor_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Look for unlicensed activities or violations
            def extract_violations_recursive(obj, path="", person_name=None):
                if isinstance(obj, dict):
                    # Extract person name if available
                    current_name = obj.get("name") or person_name
                    if current_name:
                        current_name = current_name.replace("_", " ").title()

                    # Check for confirmed unlicensed status
                    confirmed_unlicensed = obj.get("confirmed_unlicensed", False)
                    status = str(obj.get("status", "")).lower()
                    result = str(obj.get("result", "")).lower()

                    # Check for "no license" patterns
                    is_unlicensed = (
                        confirmed_unlicensed or
                        "not_found" in status or
                        "no license" in result or
                        "no_license" in result or
                        "not found" in result
                    )

                    if is_unlicensed and current_name:
                        key_id = f"{current_name}_dpor_unlicensed_virginia"

                        if key_id.lower() not in self.existing_violations:
                            # Get jurisdiction from path or state field
                            jurisdiction = "Virginia"
                            if "tx" in path.lower():
                                jurisdiction = "Texas"
                            elif "md" in path.lower():
                                jurisdiction = "Maryland"
                            elif "dc" in path.lower():
                                jurisdiction = "District of Columbia"

                            violations.append({
                                "violation_type": f"Unlicensed Practice ({jurisdiction})",
                                "entity_name": current_name,
                                "source": "va_dpor_complaint",
                                "severity": "HIGH",
                                "description": f"DPOR verification confirms no license found for {current_name} in {jurisdiction}",
                                "jurisdiction": jurisdiction,
                                "verified_date": obj.get("verified_date") or obj.get("search_date", ""),
                                "search_result": obj.get("result", "")
                            })

                    # Recursively check nested structures
                    for k, v in obj.items():
                        extract_violations_recursive(v, f"{path}.{k}" if path else k, current_name or person_name)

                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        extract_violations_recursive(item, f"{path}[{i}]", person_name)

            # Check personnel_list structure
            if "personnel_list" in data:
                for person in data["personnel_list"]:
                    person_name = person.get("name", "").replace("_", " ").title()
                    if person_name:
                        # Check license_verification section
                        license_verification = person.get("license_verification", {})
                        extract_violations_recursive(license_verification, "license_verification", person_name)
            else:
                # Fallback: recursive search
                extract_violations_recursive(data)

        except Exception as e:
            print(f"⚠️  Error processing DPOR data: {e}")
            import traceback
            traceback.print_exc()

        print(f"   Found {len(violations)} new violations in DPOR data")
        return violations

    def discover_from_embeddings(self, embeddings_file: Path) -> List[Dict[str, Any]]:
        """Use ML embeddings to discover similar violation patterns (batch processing)"""
        print(f"\n🔍 Using ML to discover violations from embeddings (batch processing)...")
        violations = []

        try:
            with open(embeddings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Get existing violation embeddings for comparison
            existing_violation_texts = []
            for category, items in self.violations.get("violations", {}).items():
                for item in items:
                    text = self._create_violation_text(item)
                    existing_violation_texts.append(text)

            if not existing_violation_texts:
                return violations

            # Batch encode existing violations (leverage 128GB RAM)
            print(f"   Encoding {len(existing_violation_texts)} existing violations...")
            existing_embeddings = self.model.encode(existing_violation_texts, normalize_embeddings=True,
                                                    batch_size=64, show_progress_bar=False)

            # Process Lariat embeddings in batches
            if "vectors" in data:
                candidate_vectors = []
                for vec in data["vectors"]:
                    text = vec.get("text", "")
                    if any(pattern in text.lower() for patterns in self.violation_patterns.values() for pattern in patterns):
                        candidate_vectors.append((vec, text))

                print(f"   Processing {len(candidate_vectors)} candidate vectors in batches...")

                # Process in batches for efficiency
                batch_size = 32
                for i in range(0, len(candidate_vectors), batch_size):
                    batch = candidate_vectors[i:i+batch_size]
                    batch_embeddings = []
                    batch_entities = []

                    for vec, text in batch:
                        if vec.get("embedding"):
                            batch_embeddings.append(np.array(vec.get("embedding")).reshape(1, -1))
                            # Extract entity info
                            entity_match = re.search(r'Name:\s*([^\n|]+)', text)
                            entity = entity_match.group(1).strip() if entity_match else None
                            batch_entities.append((vec, entity, text))

                    if batch_embeddings:
                        # Batch similarity calculation
                        batch_emb_array = np.vstack(batch_embeddings)
                        similarities = cosine_similarity(batch_emb_array, existing_embeddings)

                        for j, (vec, entity, text) in enumerate(batch_entities):
                            if entity and max(similarities[j]) > 0.7:
                                key = f"{entity}_ml_discovered_{vec.get('id', '')}"
                                if key.lower() not in self.existing_violations:
                                    violations.append({
                                        "violation_type": "ML-Discovered Violation",
                                        "entity_name": entity,
                                        "source": "ml_embedding_analysis",
                                        "similarity": float(max(similarities[j])),
                                        "severity": "MEDIUM",
                                        "description": f"ML similarity match ({max(similarities[j]):.3f}) for {entity}"
                                    })

        except Exception as e:
            print(f"⚠️  Error processing embeddings: {e}")
            import traceback
            traceback.print_exc()

        print(f"   Found {len(violations)} new violations via ML analysis")
        return violations

    def _create_violation_text(self, violation: Dict[str, Any]) -> str:
        """Create text representation of violation"""
        parts = []
        if violation.get("violation_type"):
            parts.append(f"Violation: {violation['violation_type']}")
        if violation.get("entity_name"):
            parts.append(f"Entity: {violation['entity_name']}")
        if violation.get("description"):
            parts.append(f"Description: {violation['description']}")
        return " | ".join(parts)

    def curate_violations(self, all_violations: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Curate and organize discovered violations"""
        print(f"\n📊 Curating {len(all_violations)} discovered violations...")

        curated = defaultdict(list)

        for violation in all_violations:
            violation_type = violation.get("violation_type", "Unknown")

            # Normalize violation types
            if "tax" in violation_type.lower() or "forfeiture" in violation_type.lower():
                category = "tax_forfeitures"
            elif "license" in violation_type.lower() or "unlicensed" in violation_type.lower():
                category = "licensing_violations"
            elif "filing" in violation_type.lower():
                category = "filing_violations"
            elif "forfeited" in violation_type.lower() or "entity" in violation_type.lower():
                category = "entity_violations"
            elif "fraud" in violation_type.lower():
                category = "fraud_violations"
            elif "property" in violation_type.lower():
                category = "property_violations"
            else:
                category = "other_violations"

            # Add metadata
            violation["discovered_at"] = datetime.now().isoformat()
            violation["curated"] = True

            curated[category].append(violation)

        print(f"✅ Curated into {len(curated)} categories:")
        for category, items in curated.items():
            print(f"   - {category}: {len(items)} violations")

        return dict(curated)

    def save_curated_dataset(self, curated_violations: Dict[str, List[Dict[str, Any]]], output_file: Path):
        """Save curated violations dataset"""
        print(f"\n💾 Saving curated violations dataset...")

        dataset = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0.0",
                "description": "Newly discovered and curated violations dataset",
                "total_violations": sum(len(v) for v in curated_violations.values()),
                "categories": list(curated_violations.keys())
            },
            "violations": curated_violations
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved to {output_file}")
        print(f"   Total violations: {dataset['metadata']['total_violations']}")
        print(f"   Categories: {len(curated_violations)}")


def main():
    """Main function to discover and curate new violations"""
    print("=" * 80)
    print("🔍 Violation Discovery and Curation System")
    print("=" * 80)
    print()

    system = ViolationDiscoverySystem()

    # Load existing violations
    existing_file = DATA_PROCESSED_DIR / "extracted_violations.json"
    system.load_existing_violations(existing_file)

    # Load existing violations data structure
    try:
        with open(existing_file, 'r', encoding='utf-8') as f:
            system.violations = json.load(f)
    except:
        system.violations = {"violations": {}}

    all_discovered = []

    # Discover from various sources in parallel (where possible)
    print("\n🚀 Starting parallel violation discovery...")
    import time
    start_time = time.time()

    # Use ThreadPoolExecutor for I/O-bound operations
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}

        # Submit all discovery tasks
        lariat_file = DATA_RAW_DIR / "lariat.txt"
        if lariat_file.exists():
            futures['lariat'] = executor.submit(system.discover_from_lariat_data, lariat_file)

        futures['reports'] = executor.submit(system.discover_from_research_reports, RESEARCH_DIR)
        futures['licenses'] = executor.submit(system.discover_from_license_searches, RESEARCH_DIR)

        dpor_file = RESEARCH_DIR / "va_dpor_complaint" / "personnel_license_verification.json"
        if dpor_file.exists():
            futures['dpor'] = executor.submit(system.discover_from_dpor_data, dpor_file)

        embeddings_file = DATA_VECTORS_DIR / "lariat_tx_embeddings.json"
        if embeddings_file.exists():
            futures['embeddings'] = executor.submit(system.discover_from_embeddings, embeddings_file)

        # Collect results as they complete
        for name, future in futures.items():
            try:
                result = future.result()
                all_discovered.extend(result)
                print(f"✅ {name} discovery completed: {len(result)} violations")
            except Exception as e:
                print(f"⚠️  Error in {name} discovery: {e}")

    discovery_time = time.time() - start_time
    print(f"\n⏱️  Parallel discovery completed in {discovery_time:.2f} seconds")

    # Curate violations
    curated = system.curate_violations(all_discovered)

    # Save curated dataset
    output_file = DATA_PROCESSED_DIR / "newly_discovered_violations.json"
    system.save_curated_dataset(curated, output_file)

    print("\n" + "=" * 80)
    print("✅ Violation Discovery Complete!")
    print("=" * 80)
    print(f"Total new violations discovered: {len(all_discovered)}")
    print(f"Output file: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
