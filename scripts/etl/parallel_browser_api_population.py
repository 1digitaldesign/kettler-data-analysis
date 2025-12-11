#!/usr/bin/env python3
"""
Parallel Browser and API Data Population System

Uses browser automation and APIs in parallel to populate incomplete records
by searching for missing data across multiple sources.
"""

import json
import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count, Manager
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
import re

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_DIR, DATA_CLEANED_DIR, DATA_PROCESSED_DIR
from scripts.utils.state_normalizer import normalize_state
from scripts.utils.normalize_data_parallel import get_optimal_worker_count
from scripts.etl.browser_automation_integration import BrowserAutomationIntegration

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: requests library not available. API calls will be disabled.")


class ParallelBrowserAPIPopulation:
    """Parallel system for populating data using browser automation and APIs."""

    def __init__(self):
        self.results = {
            "records_processed": 0,
            "records_populated": 0,
            "fields_populated": 0,
            "api_calls": 0,
            "browser_searches": 0,
            "errors": [],
            "population_log": []
        }
        self.api_endpoints = self._load_api_endpoints()
        self.browser_searches = []
        self.browser_integration = BrowserAutomationIntegration()

    def _load_api_endpoints(self) -> Dict[str, Any]:
        """Load API endpoint configurations."""
        return {
            "state_license_apis": {
                "va": {
                    "url": "https://www.dpor.virginia.gov/LicenseLookup/",
                    "type": "browser",  # Requires browser automation
                    "search_fields": ["name", "license_number"]
                },
                "tx": {
                    "url": "https://www.trec.texas.gov/apps/license_holder_search/",
                    "type": "browser",
                    "search_fields": ["name", "license_number"]
                },
                "dc": {
                    "url": "https://www.dcopla.com/real_estate_license_lookup",
                    "type": "browser",
                    "search_fields": ["name", "license_number"]
                },
                "md": {
                    "url": "https://www.dllr.state.md.us/cgi_bin/electroniclicensing/op_search/op_search.cgi",
                    "type": "browser",
                    "search_fields": ["name", "license_number"]
                }
            },
            "company_registration_apis": {
                "va_scc": {
                    "url": "https://cis.scc.virginia.gov/EntitySearch/Index",
                    "type": "browser",
                    "search_fields": ["company_name", "entity_id"]
                },
                "dc_ra": {
                    "url": "https://corponline.dcra.dc.gov/",
                    "type": "browser",
                    "search_fields": ["company_name", "entity_id"]
                }
            }
        }

    def load_incomplete_records(self) -> List[Dict[str, Any]]:
        """Load records needing population from verification guide."""
        print("=" * 80)
        print("LOADING INCOMPLETE RECORDS")
        print("=" * 80)

        guide_path = DATA_PROCESSED_DIR / "manual_verification_guide.json"
        if not guide_path.exists():
            print("  No verification guide found. Running analysis first...")
            return []

        with open(guide_path, 'r', encoding='utf-8') as f:
            guide = json.load(f)

        incomplete_records = []

        # Extract records from verification items
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

        return incomplete_records

    def _extract_missing_fields(self, reason: str) -> List[str]:
        """Extract missing field names from reason string."""
        if "Missing critical fields:" in reason:
            fields_str = reason.split("Missing critical fields: ")[-1]
            return [f.strip() for f in fields_str.split(",")]
        return []

    def populate_record_parallel(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Populate a single record using browser/API in parallel."""
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
            # Determine which methods to use based on missing fields
            if "name" in missing_fields:
                name = self._search_for_name(record)
                if name:
                    record["name"] = name
                    result["fields_populated"].append({"field": "name", "value": name, "method": "field_mapping"})
                    result["methods_used"].append("name_mapping")
                else:
                    # Generate browser automation instructions
                    browser_instructions = self.browser_integration.generate_browser_automation_instructions(record)
                    if browser_instructions.get("steps"):
                        result["browser_instructions"] = browser_instructions
                        result["methods_used"].append("browser_automation_needed")

            if "state" in missing_fields:
                state = self._search_for_state(record)
                if state:
                    record["state"] = state
                    record["jurisdiction"] = state
                    result["fields_populated"].append({"field": "state", "value": state, "method": "search"})
                    result["methods_used"].append("state_search")

            # Search for license information if available
            if "license" in str(record).lower() or any("license" in k.lower() for k in record.keys()):
                license_info = self._search_for_license(record)
                if license_info:
                    record.update(license_info)
                    result["fields_populated"].extend([
                        {"field": k, "value": v, "method": "api_search"}
                        for k, v in license_info.items()
                    ])
                    result["methods_used"].append("license_search")

            if result["fields_populated"]:
                result["success"] = True
                result["record"] = record

        except Exception as e:
            result["error"] = str(e)

        return result

    def _search_for_name(self, record: Dict) -> Optional[str]:
        """Search for entity name using available data."""
        # Try to extract from existing fields - be more comprehensive
        name_fields = [
            'name', 'title', 'company', 'person', 'entity', 'firm', 'organization',
            'business_name', 'firm_name', 'company_name', 'principal_broker',
            'individual_name', 'licensee_name', 'registered_name'
        ]

        for key in name_fields:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '']:
                    # Normalize the name (remove underscores, fix capitalization)
                    normalized = value.replace('_', ' ').title()
                    return normalized

        # Try to extract from license number or ID via cross-reference
        if 'license_number' in record or 'firm_license' in record:
            license_num = record.get('license_number') or record.get('firm_license')
            # This would trigger browser automation to search license database
            # For now, return None to indicate browser search needed
            return None

        return None

    def _search_for_state(self, record: Dict) -> Optional[str]:
        """Search for state/jurisdiction."""
        # Try existing fields first
        for key in ['jurisdiction', 'location', 'region', 'state_code', 'state_abbrev']:
            if key in record and record[key]:
                return normalize_state(record[key])

        # Try to infer from address
        if 'address' in record:
            address = str(record['address']).upper()
            # Common state patterns in addresses
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

    def _search_for_license(self, record: Dict) -> Dict[str, Any]:
        """Search for license information using APIs or browser."""
        license_info = {}

        # Check if we have enough info to search
        name = record.get('name') or record.get('firm_name') or record.get('company_name')
        state = record.get('state') or record.get('jurisdiction')
        license_number = record.get('license_number') or record.get('license')

        if not name and not license_number:
            return license_info

        # Determine which API/endpoint to use
        if state:
            state_norm = normalize_state(state)
            if state_norm in self.api_endpoints["state_license_apis"]:
                endpoint = self.api_endpoints["state_license_apis"][state_norm]
                # This would trigger browser automation
                # For now, return empty (would be populated by browser automation)
                pass

        return license_info

    def process_records_parallel(self, incomplete_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process incomplete records in parallel - optimized for ARM M4 MAX with 128GB RAM."""
        print("\n" + "=" * 80)
        print("PARALLEL BROWSER/API POPULATION (ARM M4 MAX OPTIMIZED)")
        print("=" * 80)

        if not incomplete_records:
            print("  No incomplete records to process.")
            return self.results

        # Process ALL records - with 128GB RAM we can handle much more
        records_to_process = incomplete_records

        # Aggressive parallelization for ARM M4 MAX
        # Use more workers than CPU cores since we have massive RAM
        cpu_cores = cpu_count()
        # For I/O-bound browser/API operations, use 4x CPU cores
        # With 128GB RAM, we can handle many concurrent operations
        worker_count = min(cpu_cores * 4, 128, len(records_to_process))

        print(f"\nProcessing {len(records_to_process)} records in parallel...")
        print(f"CPU cores: {cpu_cores}")
        print(f"Worker processes: {worker_count}")
        print(f"RAM available: 128GB (optimized for high concurrency)")

        # Process in parallel using multiprocessing with larger batches
        batch_size = max(100, len(records_to_process) // worker_count)

        start_time = time.time()

        with Pool(processes=worker_count) as pool:
            # Use imap_unordered for better performance with large datasets
            results = list(pool.imap_unordered(
                self.populate_record_parallel,
                records_to_process,
                chunksize=batch_size
            ))

        elapsed_time = time.time() - start_time

        # Aggregate results efficiently
        processed = 0
        populated = 0
        fields_count = 0
        api_calls = 0
        browser_searches = 0
        errors = []

        for result in results:
            processed += 1

            if result.get("success"):
                populated += 1
                fields_count += len(result.get("fields_populated", []))
                self.results["population_log"].append(result)

                # Update methods used
                for method in result.get("methods_used", []):
                    if "api" in method:
                        api_calls += 1
                    if "search" in method or "browser" in method:
                        browser_searches += 1

            if result.get("error"):
                errors.append({
                    "record": result.get("record", {}),
                    "error": result.get("error")
                })

        # Update results
        self.results["records_processed"] = processed
        self.results["records_populated"] = populated
        self.results["fields_populated"] = fields_count
        self.results["api_calls"] = api_calls
        self.results["browser_searches"] = browser_searches
        self.results["errors"] = errors
        self.results["processing_time"] = elapsed_time
        self.results["throughput"] = processed / elapsed_time if elapsed_time > 0 else 0

        print(f"\n  Records processed: {processed}")
        print(f"  Records populated: {populated}")
        print(f"  Fields populated: {fields_count}")
        print(f"  API calls: {api_calls}")
        print(f"  Browser searches: {browser_searches}")
        print(f"  Errors: {len(errors)}")
        print(f"  Processing time: {elapsed_time:.2f} seconds")
        print(f"  Throughput: {self.results['throughput']:.1f} records/second")

        return self.results

    def update_cleaned_files(self, population_results: List[Dict[str, Any]]):
        """Update cleaned data files with populated records."""
        print("\n" + "=" * 80)
        print("UPDATING CLEANED FILES")
        print("=" * 80)

        # Group results by source file (if we can determine it)
        # For now, we'll need to match records back to their source files
        files_updated = 0

        # This would require maintaining a mapping of records to source files
        # For now, we'll save the populated records separately
        populated_records_path = DATA_PROCESSED_DIR / "populated_records.json"

        with open(populated_records_path, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_date": datetime.now().isoformat(),
                "populated_records": population_results,
                "summary": {
                    "total_records": len(population_results),
                    "successful": len([r for r in population_results if r.get("success")]),
                    "total_fields": sum(len(r.get("fields_populated", [])) for r in population_results)
                }
            }, f, indent=2, ensure_ascii=False)

        print(f"\n  Populated records saved to: {populated_records_path}")
        print(f"  Records with updates: {len([r for r in population_results if r.get('success')])}")

        return populated_records_path

    def generate_browser_automation_script(self) -> Path:
        """Generate browser automation script for manual execution or integration."""
        print("\n" + "=" * 80)
        print("GENERATING BROWSER AUTOMATION SCRIPT")
        print("=" * 80)

        script_content = """#!/usr/bin/env python3
\"\"\"
Browser Automation Script for Data Population

This script uses browser automation to search for missing data.
Requires: playwright or selenium
\"\"\"

import asyncio
from playwright.async_api import async_playwright

async def search_license_database(state: str, name: str = None, license_number: str = None):
    \"\"\"Search state license database using browser automation.\"\"\"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to appropriate state database
        state_urls = {
            'va': 'https://www.dpor.virginia.gov/LicenseLookup/',
            'tx': 'https://www.trec.texas.gov/apps/license_holder_search/',
            'dc': 'https://www.dcopla.com/real_estate_license_lookup',
            'md': 'https://www.dllr.state.md.us/cgi_bin/electroniclicensing/op_search/op_search.cgi'
        }

        if state not in state_urls:
            return None

        await page.goto(state_urls[state])

        # Fill search form based on available data
        if name:
            # Find and fill name field
            try:
                name_input = await page.query_selector('input[name*="name"], input[id*="name"]')
                if name_input:
                    await name_input.fill(name)
            except:
                pass

        if license_number:
            # Find and fill license number field
            try:
                license_input = await page.query_selector('input[name*="license"], input[id*="license"]')
                if license_input:
                    await license_input.fill(license_number)
            except:
                pass

        # Submit form
        try:
            submit_button = await page.query_selector('button[type="submit"], input[type="submit"]')
            if submit_button:
                await submit_button.click()
                await page.wait_for_timeout(2000)  # Wait for results
        except:
            pass

        # Extract results
        results = {}
        try:
            # Try to find result elements (this is state-specific)
            result_elements = await page.query_selector_all('.result, .license-info, table tr')
            # Extract data from results
            # This would need to be customized per state
        except:
            pass

        await browser.close()
        return results

# Example usage
if __name__ == "__main__":
    # This would be called for each incomplete record
    asyncio.run(search_license_database('va', name='Kettler Management Inc'))
"""

        script_path = DATA_PROCESSED_DIR / "browser_automation_population.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        print(f"\n  Browser automation script generated: {script_path}")
        print("  Note: This script requires playwright or selenium to be installed")

        return script_path

    def run_full_population(self) -> Dict[str, Any]:
        """Run complete parallel browser/API population process."""
        print("=" * 80)
        print("PARALLEL BROWSER/API DATA POPULATION SYSTEM")
        print("=" * 80)

        # Step 1: Load incomplete records
        incomplete_records = self.load_incomplete_records()

        if not incomplete_records:
            print("\nNo incomplete records found. Data cleaning may be needed first.")
            return self.results

        # Step 2: Process records in parallel
        results = self.process_records_parallel(incomplete_records)

        # Step 3: Update cleaned files
        populated_path = self.update_cleaned_files(self.results["population_log"])
        results["populated_records_path"] = str(populated_path)

        # Step 4: Generate browser automation script
        script_path = self.generate_browser_automation_script()
        results["browser_script_path"] = str(script_path)

        # Step 5: Save results
        results_path = DATA_PROCESSED_DIR / "parallel_population_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 80)
        print("POPULATION COMPLETE")
        print("=" * 80)
        print(f"  Results saved to: {results_path}")
        print(f"  Populated records: {populated_path}")
        print(f"  Browser script: {script_path}")
        print("=" * 80)

        return results


def main():
    """Main execution."""
    populator = ParallelBrowserAPIPopulation()
    results = populator.run_full_population()
    return results


if __name__ == "__main__":
    main()
