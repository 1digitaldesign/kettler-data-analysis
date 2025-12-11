#!/usr/bin/env python3
"""
Ultra-Parallel Browser Population Pipeline

Optimized for ARM M4 MAX with 128GB RAM - processes ALL incomplete records
using maximum parallelization and browser automation tools.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from multiprocessing import Pool, cpu_count, Manager
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import re

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import DATA_PROCESSED_DIR, DATA_CLEANED_DIR
from scripts.utils.state_normalizer import normalize_state
from scripts.etl.browser_automation_integration import BrowserAutomationIntegration


class UltraParallelBrowserPopulation:
    """Ultra-parallel browser population system for ARM M4 MAX."""

    def __init__(self):
        self.results = {
            "records_processed": 0,
            "records_populated": 0,
            "fields_populated": 0,
            "browser_tasks_created": 0,
            "errors": [],
            "start_time": datetime.now().isoformat()
        }
        self.browser_integration = BrowserAutomationIntegration()
        self.population_cache = {}  # Cache for field mappings

    def load_all_incomplete_records(self) -> List[Dict[str, Any]]:
        """Load ALL incomplete records - no limits with 128GB RAM."""
        print("=" * 80)
        print("LOADING ALL INCOMPLETE RECORDS")
        print("=" * 80)

        guide_path = DATA_PROCESSED_DIR / "manual_verification_guide.json"
        if not guide_path.exists():
            print("  No verification guide found.")
            return []

        with open(guide_path, 'r', encoding='utf-8') as f:
            guide = json.load(f)

        incomplete_records = []
        for item in guide.get("verification_items", []):
            record = item.get("record_preview", {})
            reason = item.get("reason", "")

            if record:
                incomplete_records.append({
                    "record": record,
                    "reason": reason,
                    "missing_fields": self._extract_missing_fields(reason),
                    "guidance": item.get("guidance", "")
                })

        print(f"\n  Loaded {len(incomplete_records)} incomplete records")
        print(f"  Records missing name: {len([r for r in incomplete_records if 'name' in r['missing_fields']])}")
        print(f"  Records missing state: {len([r for r in incomplete_records if 'state' in r['missing_fields']])}")
        print(f"  Records missing both: {len([r for r in incomplete_records if 'name' in r['missing_fields'] and 'state' in r['missing_fields']])}")

        return incomplete_records

    def _extract_missing_fields(self, reason: str) -> List[str]:
        """Extract missing field names from reason string."""
        if "Missing critical fields:" in reason:
            fields_str = reason.split("Missing critical fields: ")[-1]
            return [f.strip() for f in fields_str.split(",")]
        return []

    def populate_record_ultra_fast(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ultra-fast record population using field mapping and caching."""
        result = {
            "record": record_data.get("record", {}),
            "fields_populated": [],
            "methods_used": [],
            "success": False,
            "error": None
        }

        record = record_data.get("record", {})
        missing_fields = record_data.get("missing_fields", [])

        try:
            # Fast field mapping (no browser needed)
            if "name" in missing_fields:
                name = self._extract_name_fast(record)
                if name:
                    record["name"] = name
                    result["fields_populated"].append({
                        "field": "name",
                        "value": name,
                        "method": "field_mapping"
                    })
                    result["methods_used"].append("name_mapping")
                    result["success"] = True

            if "state" in missing_fields:
                state = self._extract_state_fast(record)
                if state:
                    record["state"] = state
                    record["jurisdiction"] = state
                    result["fields_populated"].append({
                        "field": "state",
                        "value": state,
                        "method": "field_mapping"
                    })
                    result["methods_used"].append("state_mapping")
                    result["success"] = True

            result["record"] = record

        except Exception as e:
            result["error"] = str(e)

        return result

    def _extract_name_fast(self, record: Dict) -> Optional[str]:
        """Fast name extraction with caching."""
        # Check cache first
        record_key = str(sorted(record.items()))[:100]  # Use first 100 chars as key
        if record_key in self.population_cache:
            return self.population_cache[record_key].get("name")

        # Extract name
        name_fields = [
            'name', 'firm_name', 'company_name', 'title', 'company', 'person',
            'entity', 'firm', 'organization', 'business_name', 'principal_broker',
            'individual_name', 'licensee_name', 'registered_name'
        ]

        for key in name_fields:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '']:
                    normalized = value.replace('_', ' ').title()
                    # Cache result
                    self.population_cache[record_key] = {"name": normalized}
                    return normalized

        return None

    def _extract_state_fast(self, record: Dict) -> Optional[str]:
        """Fast state extraction with caching."""
        # Check cache first
        record_key = str(sorted(record.items()))[:100]
        if record_key in self.population_cache:
            return self.population_cache[record_key].get("state")

        # Extract state
        for key in ['state', 'jurisdiction', 'location', 'region']:
            if key in record and record[key]:
                state = normalize_state(record[key])
                self.population_cache[record_key] = {"state": state}
                return state

        # Extract from address
        if 'address' in record:
            address = str(record['address']).upper()
            state_patterns = {
                'VA': r'\bVA\b|\bVIRGINIA\b',
                'TX': r'\bTX\b|\bTEXAS\b',
                'MD': r'\bMD\b|\bMARYLAND\b',
                'DC': r'\bDC\b|\bD\.C\.\b|\bDISTRICT OF COLUMBIA\b',
                'NC': r'\bNC\b|\bNORTH CAROLINA\b',
                'PA': r'\bPA\b|\bPENNSYLVANIA\b',
                'NY': r'\bNY\b|\bNEW YORK\b',
                'NJ': r'\bNJ\b|\bNEW JERSEY\b',
                'CT': r'\bCT\b|\bCONNECTICUT\b',
                'MA': r'\bMA\b|\bMASSACHUSETTS\b'
            }

            for state_code, pattern in state_patterns.items():
                if re.search(pattern, address):
                    state = normalize_state(state_code)
                    self.population_cache[record_key] = {"state": state}
                    return state

        return None

    def process_all_ultra_parallel(self) -> Dict[str, Any]:
        """Process ALL records with maximum parallelization."""
        print("\n" + "=" * 80)
        print("ULTRA-PARALLEL PROCESSING (ARM M4 MAX - 128GB RAM)")
        print("=" * 80)

        # Load ALL incomplete records
        incomplete_records = self.load_all_incomplete_records()

        if not incomplete_records:
            print("  No incomplete records found.")
            return self.results

        total_records = len(incomplete_records)
        print(f"\nProcessing ALL {total_records} records...")

        # Maximum parallelization for ARM M4 MAX
        cpu_cores = cpu_count()
        # Use 32x CPU cores for maximum throughput
        # With 128GB RAM, each worker uses minimal memory
        max_workers = min(cpu_cores * 32, 1024, total_records)

        print(f"CPU cores: {cpu_cores}")
        print(f"Worker processes: {max_workers}")
        print(f"RAM: 128GB (ultra-high concurrency)")
        print(f"Chunk size: {max(1, total_records // max_workers)}")

        start_time = time.time()

        # Process with maximum parallelization
        with Pool(processes=max_workers) as pool:
            # Use imap_unordered for maximum efficiency
            results = list(pool.imap_unordered(
                self.populate_record_ultra_fast,
                incomplete_records,
                chunksize=max(1, total_records // max_workers)
            ))

        elapsed_time = time.time() - start_time

        # Aggregate results efficiently
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

        # Update results
        self.results["records_processed"] = processed
        self.results["records_populated"] = populated
        self.results["fields_populated"] = fields_count
        self.results["errors"] = errors[:100]  # Keep first 100 errors
        self.results["population_log"] = population_log
        self.results["processing_time"] = elapsed_time
        self.results["throughput"] = processed / elapsed_time if elapsed_time > 0 else 0
        self.results["end_time"] = datetime.now().isoformat()

        print(f"\n  Records processed: {processed}")
        print(f"  Records populated: {populated} ({populated/processed*100:.1f}%)")
        print(f"  Fields populated: {fields_count}")
        print(f"  Errors: {len(errors)}")
        print(f"  Processing time: {elapsed_time:.2f} seconds")
        print(f"  Throughput: {self.results['throughput']:.1f} records/second")

        return self.results

    def update_cleaned_files_batch(self):
        """Update cleaned files in batches for efficiency."""
        print("\n" + "=" * 80)
        print("UPDATING CLEANED FILES (BATCH MODE)")
        print("=" * 80)

        # Group populated records by source file pattern
        files_to_update = {}

        for result in self.results["population_log"]:
            record = result.get("record", {})

            # Determine source file based on record characteristics
            if 'firm_name' in record or 'firm_license' in record:
                file_key = "firms"
            elif 'license' in str(record).lower():
                file_key = "licenses"
            else:
                file_key = "other"

            if file_key not in files_to_update:
                files_to_update[file_key] = []
            files_to_update[file_key].append(record)

        # Save updated records
        updated_records_path = DATA_PROCESSED_DIR / "ultra_parallel_populated_records.json"
        with open(updated_records_path, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_date": datetime.now().isoformat(),
                "summary": {
                    "total_records": len(self.results["population_log"]),
                    "fields_populated": self.results["fields_populated"],
                    "processing_time": self.results["processing_time"],
                    "throughput": self.results["throughput"]
                },
                "records_by_category": files_to_update,
                "all_populated_records": self.results["population_log"][:1000]  # First 1000
            }, f, indent=2, ensure_ascii=False)

        print(f"\n  Updated records saved to: {updated_records_path}")
        print(f"  Categories: {len(files_to_update)}")
        for category, records in files_to_update.items():
            print(f"    - {category}: {len(records)} records")

        return updated_records_path

    def generate_browser_automation_batch(self) -> Path:
        """Generate browser automation tasks for records still needing browser search."""
        print("\n" + "=" * 80)
        print("GENERATING BROWSER AUTOMATION BATCH")
        print("=" * 80)

        # Find records that still need browser automation
        browser_tasks = []
        incomplete_records = self.load_all_incomplete_records()

        # Check which records weren't fully populated
        populated_record_keys = {
            str(sorted(r.get("record", {}).items()))[:100]
            for r in self.results["population_log"]
            if r.get("success")
        }

        for record_data in incomplete_records:
            record_key = str(sorted(record_data.get("record", {}).items()))[:100]
            if record_key not in populated_record_keys:
                record = record_data.get("record", {})
                missing_fields = record_data.get("missing_fields", [])

                # Generate browser instructions for remaining missing fields
                if missing_fields:
                    browser_instructions = self.browser_integration.generate_browser_automation_instructions(record)
                    if browser_instructions.get("steps"):
                        browser_tasks.append({
                            "record": record,
                            "missing_fields": missing_fields,
                            "instructions": browser_instructions,
                            "priority": "high" if "name" in missing_fields and "state" in missing_fields else "medium"
                        })

        # Save browser task queue
        queue_path = DATA_PROCESSED_DIR / "browser_automation_batch_queue.json"
        with open(queue_path, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_date": datetime.now().isoformat(),
                "total_tasks": len(browser_tasks),
                "high_priority": len([t for t in browser_tasks if t.get("priority") == "high"]),
                "medium_priority": len([t for t in browser_tasks if t.get("priority") == "medium"]),
                "tasks": browser_tasks[:2000]  # First 2000 tasks
            }, f, indent=2, ensure_ascii=False)

        print(f"\n  Browser task queue generated: {queue_path}")
        print(f"  Total tasks: {len(browser_tasks)}")
        print(f"  High priority: {len([t for t in browser_tasks if t.get('priority') == 'high'])}")
        print(f"  Medium priority: {len([t for t in browser_tasks if t.get('priority') == 'medium'])}")

        self.results["browser_tasks_created"] = len(browser_tasks)
        return queue_path

    def run_ultra_parallel_pipeline(self) -> Dict[str, Any]:
        """Run complete ultra-parallel pipeline."""
        print("=" * 80)
        print("ULTRA-PARALLEL BROWSER POPULATION PIPELINE")
        print("=" * 80)
        print(f"Start time: {self.results['start_time']}")
        print()

        # Step 1: Process all records in parallel
        results = self.process_all_ultra_parallel()

        # Step 2: Update cleaned files
        updated_path = self.update_cleaned_files_batch()
        results["updated_records_path"] = str(updated_path)

        # Step 3: Generate browser automation batch
        queue_path = self.generate_browser_automation_batch()
        results["browser_queue_path"] = str(queue_path)

        # Step 4: Save complete results
        results_path = DATA_PROCESSED_DIR / "ultra_parallel_population_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 80)
        print("ULTRA-PARALLEL PIPELINE COMPLETE")
        print("=" * 80)
        print(f"  Records processed: {results['records_processed']}")
        print(f"  Records populated: {results['records_populated']}")
        print(f"  Fields populated: {results['fields_populated']}")
        print(f"  Throughput: {results['throughput']:.1f} records/second")
        print(f"  Processing time: {results['processing_time']:.2f} seconds")
        print(f"  Results: {results_path}")
        print(f"  Browser queue: {queue_path}")
        print("=" * 80)

        return results


def main():
    """Main execution."""
    pipeline = UltraParallelBrowserPopulation()
    results = pipeline.run_ultra_parallel_pipeline()
    return results


if __name__ == "__main__":
    main()
