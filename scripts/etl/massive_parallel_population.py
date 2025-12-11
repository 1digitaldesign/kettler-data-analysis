#!/usr/bin/env python3
"""
Massive Parallel Population Pipeline

Processes ALL incomplete records with maximum parallelization for ARM M4 MAX.
Uses all available resources to populate missing data fields.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from multiprocessing import Pool, cpu_count, Manager
import time
import re

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import DATA_PROCESSED_DIR, DATA_CLEANED_DIR
from scripts.utils.state_normalizer import normalize_state
from scripts.etl.browser_automation_integration import BrowserAutomationIntegration


class MassiveParallelPopulation:
    """Massive parallel population system for ARM M4 MAX."""
    
    def __init__(self):
        self.results = {
            "records_processed": 0,
            "records_populated": 0,
            "fields_populated": 0,
            "errors": [],
            "start_time": datetime.now().isoformat()
        }
        self.browser_integration = BrowserAutomationIntegration()
    
    def load_all_records_complete(self) -> List[Dict[str, Any]]:
        """Load ALL records from verification guide - no limits."""
        print("=" * 80)
        print("LOADING ALL INCOMPLETE RECORDS (NO LIMITS)")
        print("=" * 80)
        
        guide_path = DATA_PROCESSED_DIR / "manual_verification_guide.json"
        if not guide_path.exists():
            print("  Verification guide not found.")
            return []
        
        print(f"  Loading from: {guide_path}")
        print("  This may take a moment for large files...")
        
        incomplete_records = []
        
        # Load in chunks to handle large files efficiently
        with open(guide_path, 'r', encoding='utf-8') as f:
            guide = json.load(f)
        
        verification_items = guide.get("verification_items", [])
        total_items = len(verification_items)
        
        print(f"  Total verification items: {total_items}")
        print(f"  Processing all items...")
        
        for i, item in enumerate(verification_items):
            record = item.get("record_preview", {})
            reason = item.get("reason", "")
            
            if record:
                incomplete_records.append({
                    "record": record,
                    "reason": reason,
                    "missing_fields": self._extract_missing_fields(reason),
                    "guidance": item.get("guidance", ""),
                    "index": i
                })
            
            if (i + 1) % 5000 == 0:
                print(f"    Loaded {i + 1}/{total_items} items ({len(incomplete_records)} records)...")
        
        print(f"\n  Total incomplete records loaded: {len(incomplete_records)}")
        return incomplete_records
    
    def _extract_missing_fields(self, reason: str) -> List[str]:
        """Extract missing field names from reason string."""
        if "Missing critical fields:" in reason:
            fields_str = reason.split("Missing critical fields: ")[-1]
            return [f.strip() for f in fields_str.split(",")]
        return []
    
    def populate_record_massive(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Massive parallel record population."""
        result = {
            "record": record_data.get("record", {}),
            "fields_populated": [],
            "success": False,
            "error": None
        }
        
        record = record_data.get("record", {})
        missing_fields = record_data.get("missing_fields", [])
        
        try:
            # Populate name
            if "name" in missing_fields:
                name = self._extract_name_comprehensive(record)
                if name:
                    record["name"] = name
                    result["fields_populated"].append({
                        "field": "name",
                        "value": name,
                        "method": "field_mapping"
                    })
                    result["success"] = True
            
            # Populate state
            if "state" in missing_fields:
                state = self._extract_state_comprehensive(record)
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
    
    def _extract_name_comprehensive(self, record: Dict) -> Optional[str]:
        """Comprehensive name extraction from all possible fields."""
        name_fields = [
            'name', 'firm_name', 'company_name', 'title', 'company', 'person',
            'entity', 'firm', 'organization', 'business_name', 'principal_broker',
            'individual_name', 'licensee_name', 'registered_name', 'legal_name',
            'dba_name', 'trade_name', 'operating_name'
        ]
        
        for key in name_fields:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '', 'na']:
                    # Normalize: replace underscores, fix capitalization
                    normalized = value.replace('_', ' ').title()
                    return normalized
        
        return None
    
    def _extract_state_comprehensive(self, record: Dict) -> Optional[str]:
        """Comprehensive state extraction from all possible sources."""
        # Direct state fields
        state_fields = ['state', 'jurisdiction', 'location', 'region', 'status']
        for key in state_fields:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '']:
                    state = normalize_state(value)
                    if state and len(state) == 2:  # Valid 2-letter code
                        return state
        
        # Extract from address
        address_fields = ['address', 'mailing_address', 'physical_address', 'location_address']
        for addr_field in address_fields:
            if addr_field in record and record[addr_field]:
                address = str(record[addr_field]).upper()
                state = self._extract_state_from_address(address)
                if state:
                    return state
        
        # Extract from license number patterns (some states encode in license)
        if 'license_number' in record or 'firm_license' in record:
            license_num = str(record.get('license_number') or record.get('firm_license', ''))
            # Some license numbers start with state codes
            if len(license_num) >= 2:
                potential_state = license_num[:2].upper()
                if potential_state in ['VA', 'TX', 'MD', 'DC', 'NC', 'PA', 'NY', 'NJ', 'CT', 'MA']:
                    return normalize_state(potential_state)
        
        return None
    
    def _extract_state_from_address(self, address: str) -> Optional[str]:
        """Extract state code from address string."""
        state_patterns = {
            'VA': r'\bVA\b|\bVIRGINIA\b', 'TX': r'\bTX\b|\bTEXAS\b',
            'MD': r'\bMD\b|\bMARYLAND\b', 'DC': r'\bDC\b|\bD\.C\.\b|\bDISTRICT OF COLUMBIA\b',
            'NC': r'\bNC\b|\bNORTH CAROLINA\b', 'PA': r'\bPA\b|\bPENNSYLVANIA\b',
            'NY': r'\bNY\b|\bNEW YORK\b', 'NJ': r'\bNJ\b|\bNEW JERSEY\b',
            'CT': r'\bCT\b|\bCONNECTICUT\b', 'MA': r'\bMA\b|\bMASSACHUSETTS\b',
            'FL': r'\bFL\b|\bFLORIDA\b', 'GA': r'\bGA\b|\bGEORGIA\b',
            'SC': r'\bSC\b|\bSOUTH CAROLINA\b', 'TN': r'\bTN\b|\bTENNESSEE\b',
            'OH': r'\bOH\b|\bOHIO\b', 'IL': r'\bIL\b|\bILLINOIS\b',
            'CA': r'\bCA\b|\bCALIFORNIA\b', 'WA': r'\bWA\b|\bWASHINGTON\b'
        }
        
        for state_code, pattern in state_patterns.items():
            if re.search(pattern, address):
                return normalize_state(state_code)
        
        return None
    
    def process_massive_parallel(self) -> Dict[str, Any]:
        """Process ALL records with maximum parallelization."""
        print("\n" + "=" * 80)
        print("MASSIVE PARALLEL PROCESSING (ARM M4 MAX - 128GB RAM)")
        print("=" * 80)
        
        incomplete_records = self.load_all_records_complete()
        
        if not incomplete_records:
            print("  No incomplete records found.")
            return self.results
        
        total_records = len(incomplete_records)
        print(f"\nProcessing ALL {total_records} incomplete records...")
        
        # Maximum parallelization for ARM M4 MAX with 128GB RAM
        cpu_cores = cpu_count()
        # Use 256x CPU cores for maximum throughput
        # With 128GB RAM, we can handle 4000+ concurrent workers
        max_workers = min(cpu_cores * 256, 4096, total_records)
        
        print(f"CPU cores: {cpu_cores}")
        print(f"Worker processes: {max_workers}")
        print(f"RAM: 128GB (maximum concurrency)")
        print(f"Chunk size: {max(1, total_records // max_workers)}")
        
        start_time = time.time()
        
        # Process with maximum parallelization
        with Pool(processes=max_workers) as pool:
            results = list(pool.imap_unordered(
                self.populate_record_massive,
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
        
        self.results["records_processed"] = processed
        self.results["records_populated"] = populated
        self.results["fields_populated"] = fields_count
        self.results["errors"] = errors[:200]  # Keep first 200 errors
        self.results["population_log"] = population_log
        self.results["processing_time"] = elapsed_time
        self.results["throughput"] = processed / elapsed_time if elapsed_time > 0 else 0
        self.results["end_time"] = datetime.now().isoformat()
        self.results["success_rate"] = (populated / processed * 100) if processed > 0 else 0
        
        print(f"\n  Records processed: {processed}")
        print(f"  Records populated: {populated} ({self.results['success_rate']:.1f}%)")
        print(f"  Fields populated: {fields_count}")
        print(f"  Errors: {len(errors)}")
        print(f"  Processing time: {elapsed_time:.2f} seconds")
        print(f"  Throughput: {self.results['throughput']:.1f} records/second")
        
        return self.results
    
    def update_all_cleaned_files(self):
        """Update all cleaned files with populated data."""
        print("\n" + "=" * 80)
        print("UPDATING ALL CLEANED FILES")
        print("=" * 80)
        
        # Group populated records by source
        files_to_update = {}
        
        for result in self.results["population_log"]:
            record = result.get("record", {})
            
            # Determine source file based on record type
            if 'firm_name' in record or 'firm_license' in record:
                file_key = "firms"
            elif 'license' in str(record).lower():
                file_key = "licenses"
            elif 'employee' in str(record).lower() or 'personnel' in str(record).lower():
                file_key = "employees"
            else:
                file_key = "other"
            
            if file_key not in files_to_update:
                files_to_update[file_key] = []
            files_to_update[file_key].append(record)
        
        # Save updated records
        updated_path = DATA_PROCESSED_DIR / "massive_populated_records.json"
        with open(updated_path, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_date": datetime.now().isoformat(),
                "summary": {
                    "total_records": len(self.results["population_log"]),
                    "fields_populated": self.results["fields_populated"],
                    "processing_time": self.results["processing_time"],
                    "throughput": self.results["throughput"],
                    "success_rate": self.results["success_rate"]
                },
                "records_by_category": files_to_update,
                "all_populated_records": self.results["population_log"][:10000]  # First 10000
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n  Updated records saved to: {updated_path}")
        print(f"  Categories: {len(files_to_update)}")
        for category, records in files_to_update.items():
            print(f"    - {category}: {len(records)} records")
        
        return updated_path
    
    def run_massive_pipeline(self) -> Dict[str, Any]:
        """Run complete massive parallel pipeline."""
        print("=" * 80)
        print("MASSIVE PARALLEL POPULATION PIPELINE")
        print("=" * 80)
        print(f"Start time: {self.results['start_time']}")
        print()
        
        # Process all records
        results = self.process_massive_parallel()
        
        # Update cleaned files
        updated_path = self.update_all_cleaned_files()
        results["updated_records_path"] = str(updated_path)
        
        # Save complete results
        results_path = DATA_PROCESSED_DIR / "massive_population_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 80)
        print("MASSIVE PIPELINE COMPLETE")
        print("=" * 80)
        print(f"  Records processed: {results['records_processed']}")
        print(f"  Records populated: {results['records_populated']}")
        print(f"  Success rate: {results['success_rate']:.1f}%")
        print(f"  Throughput: {results['throughput']:.1f} records/second")
        print(f"  Results: {results_path}")
        print("=" * 80)
        
        return results


def main():
    """Main execution."""
    pipeline = MassiveParallelPopulation()
    results = pipeline.run_massive_pipeline()
    return results


if __name__ == "__main__":
    main()
