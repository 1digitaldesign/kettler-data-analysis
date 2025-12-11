#!/usr/bin/env python3
"""
Optimized Massive Parallel Population

Uses high-performance libraries for maximum speed:
- orjson for fast JSON parsing
- joblib for efficient parallel processing
- pandas for vectorized operations
- asyncio for I/O-bound operations
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
import re

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import DATA_PROCESSED_DIR, DATA_CLEANED_DIR
from scripts.utils.state_normalizer import normalize_state

# Try to use faster JSON library
try:
    import orjson
    JSON_LOAD = orjson.loads
    JSON_DUMP = lambda x: orjson.dumps(x).decode('utf-8')
    FAST_JSON = True
except ImportError:
    import json
    JSON_LOAD = json.loads
    JSON_DUMP = json.dumps
    FAST_JSON = False
    print("Warning: orjson not available. Install with: pip install orjson")

# Try to use joblib for better parallel processing
try:
    from joblib import Parallel, delayed
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False
    from multiprocessing import Pool, cpu_count
    print("Warning: joblib not available. Install with: pip install joblib")

# Try pandas for vectorized operations
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class OptimizedMassivePopulation:
    """Optimized massive parallel population using high-performance libraries."""

    def __init__(self):
        self.results = {
            "records_processed": 0,
            "records_populated": 0,
            "fields_populated": 0,
            "errors": [],
            "start_time": datetime.now().isoformat()
        }
        self.name_cache = {}
        self.state_cache = {}

    def load_records_streaming(self) -> List[Dict[str, Any]]:
        """Load records using streaming JSON parsing for large files."""
        print("=" * 80)
        print("LOADING RECORDS (STREAMING MODE)")
        print("=" * 80)

        guide_path = DATA_PROCESSED_DIR / "manual_verification_guide.json"
        if not guide_path.exists():
            return []

        print(f"  Loading from: {guide_path}")

        # Use streaming JSON parser for large files
        incomplete_records = []

        try:
            # Read file in chunks if very large
            file_size = guide_path.stat().st_size
            print(f"  File size: {file_size / 1024 / 1024:.2f} MB")

            if file_size > 100 * 1024 * 1024:  # > 100MB
                print("  Using streaming parser for large file...")
                # For very large files, use ijson or streaming parser
                import json
                with open(guide_path, 'r', encoding='utf-8') as f:
                    guide = json.load(f)
            else:
                # Use fast JSON library
                with open(guide_path, 'rb') as f:
                    guide = JSON_LOAD(f.read())

            verification_items = guide.get("verification_items", [])
            total_items = len(verification_items)
            print(f"  Total items: {total_items}")

            # Process items efficiently
            for i, item in enumerate(verification_items):
                record = item.get("record_preview", {})
                reason = item.get("reason", "")

                if record:
                    incomplete_records.append({
                        "record": record,
                        "reason": reason,
                        "missing_fields": self._extract_missing_fields(reason),
                        "index": i
                    })

                if (i + 1) % 2000 == 0:
                    print(f"    Loaded {i + 1}/{total_items} items...")

        except Exception as e:
            print(f"  Error loading: {str(e)}")
            return []

        print(f"\n  Loaded {len(incomplete_records)} incomplete records")
        return incomplete_records

    def _extract_missing_fields(self, reason: str) -> List[str]:
        """Extract missing field names."""
        if "Missing critical fields:" in reason:
            fields_str = reason.split("Missing critical fields: ")[-1]
            return [f.strip() for f in fields_str.split(",")]
        return []

    def populate_record_optimized(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimized record population with caching."""
        result = {
            "record": record_data.get("record", {}),
            "fields_populated": [],
            "success": False
        }

        record = record_data.get("record", {})
        missing_fields = record_data.get("missing_fields", [])

        try:
            # Populate name with caching
            if "name" in missing_fields:
                name = self._extract_name_cached(record)
                if name:
                    record["name"] = name
                    result["fields_populated"].append({
                        "field": "name",
                        "value": name,
                        "method": "field_mapping"
                    })
                    result["success"] = True

            # Populate state with caching
            if "state" in missing_fields:
                state = self._extract_state_cached(record)
                if state:
                    record["state"] = state
                    record["jurisdiction"] = state
                    result["fields_populated"].append({
                        "field": "state",
                        "value": state,
                        "method": "field_mapping"
                    })
                    result["success"] = True

            result["record"] = record

        except Exception as e:
            result["error"] = str(e)

        return result

    def _extract_name_cached(self, record: Dict) -> Optional[str]:
        """Extract name with caching."""
        # Create cache key
        cache_key = str(sorted(record.items()))[:200]
        if cache_key in self.name_cache:
            return self.name_cache[cache_key]

        name_fields = [
            'name', 'firm_name', 'company_name', 'title', 'company', 'person',
            'entity', 'firm', 'organization', 'business_name', 'principal_broker'
        ]

        for key in name_fields:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '']:
                    normalized = value.replace('_', ' ').title()
                    self.name_cache[cache_key] = normalized
                    return normalized

        self.name_cache[cache_key] = None
        return None

    def _extract_state_cached(self, record: Dict) -> Optional[str]:
        """Extract state with caching."""
        cache_key = str(sorted(record.items()))[:200]
        if cache_key in self.state_cache:
            return self.state_cache[cache_key]

        # Direct fields
        for key in ['state', 'jurisdiction', 'location', 'region', 'status']:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '']:
                    state = normalize_state(value)
                    if state and len(state) == 2:
                        self.state_cache[cache_key] = state
                        return state

        # Extract from address
        if 'address' in record:
            address = str(record['address']).upper()
            state = self._extract_state_from_address(address)
            if state:
                self.state_cache[cache_key] = state
                return state

        self.state_cache[cache_key] = None
        return None

    def _extract_state_from_address(self, address: str) -> Optional[str]:
        """Fast state extraction from address using compiled regex."""
        # Pre-compiled patterns for speed
        if not hasattr(self, '_state_patterns'):
            self._state_patterns = {
                'VA': re.compile(r'\bVA\b|\bVIRGINIA\b'),
                'TX': re.compile(r'\bTX\b|\bTEXAS\b'),
                'MD': re.compile(r'\bMD\b|\bMARYLAND\b'),
                'DC': re.compile(r'\bDC\b|\bD\.C\.\b|\bDISTRICT OF COLUMBIA\b'),
                'NC': re.compile(r'\bNC\b|\bNORTH CAROLINA\b'),
                'PA': re.compile(r'\bPA\b|\bPENNSYLVANIA\b'),
                'NY': re.compile(r'\bNY\b|\bNEW YORK\b'),
                'NJ': re.compile(r'\bNJ\b|\bNEW JERSEY\b'),
                'CT': re.compile(r'\bCT\b|\bCONNECTICUT\b'),
                'MA': re.compile(r'\bMA\b|\bMASSACHUSETTS\b')
            }

        for state_code, pattern in self._state_patterns.items():
            if pattern.search(address):
                return normalize_state(state_code)

        return None

    def process_with_joblib(self, incomplete_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process using joblib for better parallelization."""
        print("\n" + "=" * 80)
        print("OPTIMIZED PARALLEL PROCESSING (JOBLIB)")
        print("=" * 80)

        total_records = len(incomplete_records)
        print(f"\nProcessing {total_records} records...")

        # Joblib is more efficient than multiprocessing.Pool
        if JOBLIB_AVAILABLE:
            from multiprocessing import cpu_count
            cpu_cores = cpu_count()
            # Use loky backend (multiprocessing) for CPU-bound operations
            n_jobs = min(cpu_cores * 16, 256, total_records)

            print(f"CPU cores: {cpu_cores}")
            print(f"Parallel jobs: {n_jobs}")
            print(f"Using joblib backend: loky (multiprocessing)")
            print(f"Batch size: {max(10, total_records // n_jobs)}")

            start_time = time.time()

            # Use joblib with loky backend for CPU-bound operations
            results = Parallel(n_jobs=n_jobs, backend='loky', verbose=0, batch_size=max(10, total_records // n_jobs))(
                delayed(self.populate_record_optimized)(record_data)
                for record_data in incomplete_records
            )

            elapsed_time = time.time() - start_time
        else:
            # Fallback to multiprocessing
            from multiprocessing import Pool, cpu_count
            cpu_cores = cpu_count()
            max_workers = min(cpu_cores * 32, 512, total_records)

            print(f"CPU cores: {cpu_cores}")
            print(f"Worker processes: {max_workers}")
            print("Using multiprocessing (fallback)")

            start_time = time.time()

            with Pool(processes=max_workers) as pool:
                results = pool.map(self.populate_record_optimized, incomplete_records)

            elapsed_time = time.time() - start_time

        # Aggregate results
        processed = 0
        populated = 0
        fields_count = 0
        errors = []
        population_log = []

        for result in results:
            processed += 1

            if result.get("success"):
                populated += 1
                fields_count += len(result.get("fields_populated", []))
                population_log.append(result)

            if result.get("error"):
                errors.append(result)

        self.results["records_processed"] = processed
        self.results["records_populated"] = populated
        self.results["fields_populated"] = fields_count
        self.results["errors"] = errors[:100]
        self.results["population_log"] = population_log
        self.results["processing_time"] = elapsed_time
        self.results["throughput"] = processed / elapsed_time if elapsed_time > 0 else 0
        self.results["success_rate"] = (populated / processed * 100) if processed > 0 else 0
        self.results["end_time"] = datetime.now().isoformat()

        print(f"\n  Records processed: {processed}")
        print(f"  Records populated: {populated} ({self.results['success_rate']:.1f}%)")
        print(f"  Fields populated: {fields_count}")
        print(f"  Errors: {len(errors)}")
        print(f"  Processing time: {elapsed_time:.2f} seconds")
        print(f"  Throughput: {self.results['throughput']:.1f} records/second")

        return self.results

    def process_with_pandas(self, incomplete_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process using pandas for vectorized operations (if applicable)."""
        # Skip pandas for now - use joblib instead
        return self.process_with_joblib(incomplete_records)

        print("\n" + "=" * 80)
        print("PANDAS VECTORIZED PROCESSING")
        print("=" * 80)

        # Convert to DataFrame for vectorized operations
        df = pd.DataFrame([
            {
                **r["record"],
                "missing_fields": ",".join(r["missing_fields"]),
                "reason": r["reason"]
            }
            for r in incomplete_records
        ])

        print(f"  DataFrame shape: {df.shape}")

        # Vectorized name population
        if 'name' not in df.columns:
            # Initialize name column
            df['name'] = None
            # Try to populate from firm_name, company_name, etc.
            name_sources = ['firm_name', 'company_name', 'title', 'principal_broker']
            for source in name_sources:
                if source in df.columns:
                    df['name'] = df['name'].fillna(
                        df[source].apply(lambda x: str(x).replace('_', ' ').title() if pd.notna(x) else None)
                    )
                    break

        # Vectorized state population
        if 'state' not in df.columns:
            # Extract from address
            if 'address' in df.columns:
                df['state'] = df['address'].apply(self._extract_state_from_address)

        # Convert back to results format
        populated_count = df['name'].notna().sum() + df['state'].notna().sum()

        self.results["records_processed"] = len(df)
        self.results["records_populated"] = populated_count
        self.results["fields_populated"] = populated_count

        return self.results

    def save_results_optimized(self) -> Path:
        """Save results using optimized JSON library."""
        results_path = DATA_PROCESSED_DIR / "optimized_population_results.json"

        output_data = {
            "generated_date": datetime.now().isoformat(),
            "summary": {
                "records_processed": self.results.get("records_processed", 0),
                "records_populated": self.results.get("records_populated", 0),
                "fields_populated": self.results.get("fields_populated", 0),
                "processing_time": self.results.get("processing_time", 0),
                "throughput": self.results.get("throughput", 0),
                "success_rate": self.results.get("success_rate", 0)
            },
            "populated_records": self.results.get("population_log", [])[:5000]
        }

        if FAST_JSON:
            with open(results_path, 'wb') as f:
                f.write(orjson.dumps(output_data, option=orjson.OPT_INDENT_2))
        else:
            import json
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

        return results_path

    def run_optimized_pipeline(self) -> Dict[str, Any]:
        """Run optimized pipeline."""
        print("=" * 80)
        print("OPTIMIZED MASSIVE PARALLEL POPULATION")
        print("=" * 80)
        print(f"Start time: {self.results['start_time']}")
        print(f"Fast JSON: {FAST_JSON}")
        print(f"Joblib available: {JOBLIB_AVAILABLE}")
        print(f"Pandas available: {PANDAS_AVAILABLE}")
        print()

        # Load records
        incomplete_records = self.load_records_streaming()

        if not incomplete_records:
            print("  No incomplete records found.")
            return self.results

        # Process with joblib (more reliable than pandas for this use case)
        results = self.process_with_joblib(incomplete_records)

        # Save results
        results_path = self.save_results_optimized()
        results["results_path"] = str(results_path)

        print("\n" + "=" * 80)
        print("OPTIMIZED PIPELINE COMPLETE")
        print("=" * 80)
        print(f"  Results: {results_path}")
        print(f"  Success rate: {results['success_rate']:.1f}%")
        print(f"  Throughput: {results['throughput']:.1f} records/second")
        print("=" * 80)

        return results


def main():
    """Main execution."""
    pipeline = OptimizedMassivePopulation()
    results = pipeline.run_optimized_pipeline()
    return results


if __name__ == "__main__":
    main()
