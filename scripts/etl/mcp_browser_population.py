#!/usr/bin/env python3
"""
MCP Browser Tool Integration for Parallel Data Population

Uses MCP browser tools (@Browser) in parallel to populate incomplete records
by searching license databases and company registrations.
"""

import json
import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import DATA_PROCESSED_DIR, DATA_CLEANED_DIR
from scripts.utils.state_normalizer import normalize_state
from scripts.etl.browser_automation_integration import BrowserAutomationIntegration


class MCPBrowserPopulation:
    """Parallel browser automation using MCP browser tools."""

    def __init__(self):
        self.results = {
            "records_processed": 0,
            "records_populated": 0,
            "fields_populated": 0,
            "browser_searches": 0,
            "errors": [],
            "population_log": []
        }
        self.browser_integration = BrowserAutomationIntegration()

    def load_incomplete_records(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Load incomplete records from verification guide."""
        guide_path = DATA_PROCESSED_DIR / "manual_verification_guide.json"
        if not guide_path.exists():
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

        # Process ALL records - with 128GB RAM we can handle everything
        # Only limit if explicitly requested
        if limit:
            incomplete_records = incomplete_records[:limit]

        return incomplete_records

    def _extract_missing_fields(self, reason: str) -> List[str]:
        """Extract missing field names from reason string."""
        if "Missing critical fields:" in reason:
            fields_str = reason.split("Missing critical fields: ")[-1]
            return [f.strip() for f in fields_str.split(",")]
        return []

    def populate_with_browser(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Populate record using browser automation.
        This function is designed to be called with MCP browser tools.
        """
        result = {
            "record": record_data.get("record", {}),
            "fields_populated": [],
            "methods_used": [],
            "success": False,
            "error": None,
            "browser_instructions": None
        }

        record = record_data.get("record", {})
        missing_fields = record_data.get("missing_fields", [])

        try:
            # First, try field mapping (fast, no browser needed)
            if "name" in missing_fields:
                name = self._extract_name_from_record(record)
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
                state = self._extract_state_from_record(record)
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

            # If still missing critical fields, generate browser instructions
            remaining_missing = [f for f in missing_fields if f not in [p["field"] for p in result["fields_populated"]]]
            if remaining_missing:
                browser_instructions = self.browser_integration.generate_browser_automation_instructions(record)
                if browser_instructions.get("steps"):
                    result["browser_instructions"] = browser_instructions
                    result["methods_used"].append("browser_automation_ready")

            result["record"] = record

        except Exception as e:
            result["error"] = str(e)

        return result

    def _extract_name_from_record(self, record: Dict) -> Optional[str]:
        """Extract name from record using field mapping."""
        name_fields = [
            'name', 'firm_name', 'company_name', 'title', 'company', 'person',
            'entity', 'firm', 'organization', 'business_name', 'principal_broker'
        ]

        for key in name_fields:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '']:
                    return value.replace('_', ' ').title()
        return None

    def _extract_state_from_record(self, record: Dict) -> Optional[str]:
        """Extract state from record."""
        # Check direct state fields
        for key in ['state', 'jurisdiction', 'location', 'region']:
            if key in record and record[key]:
                return normalize_state(record[key])

        # Extract from address
        if 'address' in record:
            address = str(record['address']).upper()
            import re
            state_patterns = {
                'VA': r'\bVA\b|\bVIRGINIA\b',
                'TX': r'\bTX\b|\bTEXAS\b',
                'MD': r'\bMD\b|\bMARYLAND\b',
                'DC': r'\bDC\b|\bD\.C\.\b|\bDISTRICT OF COLUMBIA\b',
                'NC': r'\bNC\b|\bNORTH CAROLINA\b'
            }

            for state_code, pattern in state_patterns.items():
                if re.search(pattern, address):
                    return normalize_state(state_code)

        return None

    def process_all_parallel(self, max_workers: Optional[int] = None) -> Dict[str, Any]:
        """Process all incomplete records in parallel - optimized for ARM M4 MAX."""
        print("=" * 80)
        print("MCP BROWSER PARALLEL POPULATION (ARM M4 MAX - 128GB RAM)")
        print("=" * 80)

        # Load ALL incomplete records - no limits with 128GB RAM
        incomplete_records = self.load_incomplete_records(limit=None)

        if not incomplete_records:
            print("  No incomplete records found.")
            return self.results

        total_records = len(incomplete_records)
        print(f"\nLoaded ALL {total_records} incomplete records (no limits)")

        # Aggressive parallelization for ARM M4 MAX with 128GB RAM
        cpu_cores = cpu_count()
        # Use 32x CPU cores for I/O-bound operations (browser/API calls)
        # With 128GB RAM, we can handle massive concurrency
        # Each worker uses minimal memory, so we can scale aggressively
        if max_workers is None:
            # Calculate optimal workers: 32x cores for maximum throughput
            # For 16 cores: 512 workers, each handling ~1-2 records
            # With 128GB RAM, we can easily handle 1000+ concurrent workers
            max_workers = min(cpu_cores * 32, 1024, len(incomplete_records))

        print(f"CPU cores: {cpu_cores}")
        print(f"Worker processes: {max_workers}")
        print(f"RAM: 128GB (high concurrency mode)")
        print(f"\nProcessing {len(incomplete_records)} records in parallel...")

        start_time = time.time()

        # Process in parallel using multiprocessing
        with Pool(processes=max_workers) as pool:
            # Use imap_unordered for better performance
            results = list(pool.imap_unordered(
                self.populate_with_browser,
                incomplete_records,
                chunksize=max(10, len(incomplete_records) // max_workers)
            ))

        elapsed_time = time.time() - start_time

        # Aggregate results
        processed = 0
        populated = 0
        fields_count = 0
        browser_ready = 0
        errors = []

        for result in results:
            processed += 1

            if result.get("success"):
                populated += 1
                fields_count += len(result.get("fields_populated", []))
                self.results["population_log"].append(result)

            if result.get("browser_instructions"):
                browser_ready += 1
                self.results["browser_searches"] += 1

            if result.get("error"):
                errors.append(result)

        # Update results
        self.results["records_processed"] = processed
        self.results["records_populated"] = populated
        self.results["fields_populated"] = fields_count
        self.results["errors"] = errors
        self.results["browser_ready_count"] = browser_ready
        self.results["processing_time"] = elapsed_time
        self.results["throughput"] = processed / elapsed_time if elapsed_time > 0 else 0

        print(f"\n  Records processed: {processed}")
        print(f"  Records populated: {populated}")
        print(f"  Fields populated: {fields_count}")
        print(f"  Browser automation ready: {browser_ready}")
        print(f"  Errors: {len(errors)}")
        print(f"  Processing time: {elapsed_time:.2f} seconds")
        print(f"  Throughput: {self.results['throughput']:.1f} records/second")

        return self.results

    def save_results(self) -> Path:
        """Save population results."""
        results_path = DATA_PROCESSED_DIR / "mcp_browser_population_results.json"

        # Save populated records
        populated_records = [
            r for r in self.results["population_log"]
            if r.get("success")
        ]

        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_date": datetime.now().isoformat(),
                "summary": {
                    "records_processed": self.results["records_processed"],
                    "records_populated": self.results["records_populated"],
                    "fields_populated": self.results["fields_populated"],
                    "browser_ready": self.results.get("browser_ready_count", 0),
                    "processing_time": self.results.get("processing_time", 0),
                    "throughput": self.results.get("throughput", 0)
                },
                "populated_records": populated_records[:1000],  # First 1000
                "errors": self.results["errors"][:100]  # First 100 errors
            }, f, indent=2, ensure_ascii=False)

        return results_path

    def generate_browser_task_queue(self) -> Path:
        """Generate browser automation task queue for MCP tools."""
        browser_tasks = []

        for result in self.results["population_log"]:
            if result.get("browser_instructions"):
                browser_tasks.append({
                    "record": result.get("record", {}),
                    "instructions": result["browser_instructions"],
                    "missing_fields": [f for f in result.get("record", {}).keys()
                                     if result.get("record", {}).get(f) is None]
                })

        queue_path = DATA_PROCESSED_DIR / "browser_automation_queue.json"
        with open(queue_path, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_date": datetime.now().isoformat(),
                "total_tasks": len(browser_tasks),
                "tasks": browser_tasks[:500]  # First 500 tasks
            }, f, indent=2, ensure_ascii=False)

        return queue_path

    def run_full_population(self) -> Dict[str, Any]:
        """Run complete parallel population process."""
        # Process all records in parallel
        results = self.process_all_parallel()

        # Save results
        results_path = self.save_results()
        results["results_path"] = str(results_path)

        # Generate browser task queue
        queue_path = self.generate_browser_task_queue()
        results["browser_queue_path"] = str(queue_path)

        print("\n" + "=" * 80)
        print("POPULATION COMPLETE")
        print("=" * 80)
        print(f"  Results: {results_path}")
        print(f"  Browser queue: {queue_path}")
        print("=" * 80)

        return results


def main():
    """Main execution."""
    populator = MCPBrowserPopulation()
    results = populator.run_full_population()
    return results


if __name__ == "__main__":
    main()
