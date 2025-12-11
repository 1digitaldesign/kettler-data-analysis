#!/usr/bin/env python3
"""
SDLC-Based Research Data Processing Pipeline

Implements a complete Software Development Life Cycle (SDLC) approach to:
1. Clean and normalize all research/ data
2. Process and transform data for data/ directory
3. Validate data quality and consistency
4. Generate comprehensive reports

SDLC Phases:
- Phase 1: Requirements Analysis
- Phase 2: Design
- Phase 3: Implementation
- Phase 4: Testing
- Phase 5: Deployment
- Phase 6: Maintenance & Validation
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import time
import shutil

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, RESEARCH_DIR, DATA_DIR, DATA_PROCESSED_DIR, DATA_CLEANED_DIR
from scripts.utils.state_normalizer import normalize_dict_recursive, normalize_state
from scripts.utils.normalize_data_parallel import get_optimal_worker_count


class SDLCResearchDataPipeline:
    """SDLC-based pipeline for processing research data."""

    def __init__(self):
        self.results = {
            "phase1_requirements": {},
            "phase2_design": {},
            "phase3_implementation": {},
            "phase4_testing": {},
            "phase5_deployment": {},
            "phase6_validation": {},
            "metadata": {
                "start_time": datetime.now().isoformat(),
                "pipeline_version": "1.0.0"
            }
        }

    # ============================================================================
    # PHASE 1: REQUIREMENTS ANALYSIS
    # ============================================================================

    def phase1_requirements_analysis(self) -> Dict[str, Any]:
        """Phase 1: Analyze research data structure and requirements."""
        print("=" * 80)
        print("SDLC PHASE 1: REQUIREMENTS ANALYSIS")
        print("=" * 80)

        requirements = {
            "research_files_analyzed": 0,
            "data_categories": {},
            "file_types": {},
            "total_size_bytes": 0,
            "issues_found": [],
            "normalization_needed": True,
            "data_quality_issues": []
        }

        print("\nAnalyzing research directory structure...")

        # Analyze all JSON files in research/
        json_files = list(RESEARCH_DIR.rglob('*.json'))
        requirements["research_files_analyzed"] = len(json_files)

        print(f"  Found {len(json_files)} JSON files")

        # Categorize files
        for json_file in json_files:
            try:
                # Get relative path for categorization
                rel_path = json_file.relative_to(RESEARCH_DIR)
                category = str(rel_path).split('/')[0] if '/' in str(rel_path) else "root"

                requirements["data_categories"][category] = \
                    requirements["data_categories"].get(category, 0) + 1

                # Get file size
                file_size = json_file.stat().st_size
                requirements["total_size_bytes"] += file_size

                # Check file type
                ext = json_file.suffix
                requirements["file_types"][ext] = \
                    requirements["file_types"].get(ext, 0) + 1

                # Quick validation
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Check for common issues
                    if isinstance(data, dict):
                        # Check for unnormalized state references
                        data_str = json.dumps(data)
                        if 'district_of_columbia' in data_str or \
                           any(state.isupper() and len(state) == 2
                               for state in data.keys() if isinstance(state, str)):
                            requirements["normalization_needed"] = True

                except json.JSONDecodeError as e:
                    requirements["data_quality_issues"].append({
                        "file": str(json_file),
                        "issue": "invalid_json",
                        "error": str(e)
                    })

            except Exception as e:
                requirements["issues_found"].append({
                    "file": str(json_file),
                    "error": str(e)
                })

        # Print summary
        print(f"\n  Categories found: {len(requirements['data_categories'])}")
        for category, count in sorted(requirements["data_categories"].items(),
                                     key=lambda x: x[1], reverse=True)[:10]:
            print(f"    - {category}: {count} files")

        print(f"\n  Total size: {requirements['total_size_bytes'] / 1024 / 1024:.2f} MB")
        print(f"  Data quality issues: {len(requirements['data_quality_issues'])}")
        print(f"  Normalization needed: {requirements['normalization_needed']}")

        self.results["phase1_requirements"] = requirements
        return requirements

    # ============================================================================
    # PHASE 2: DESIGN
    # ============================================================================

    def phase2_design(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: Design data processing architecture."""
        print("\n" + "=" * 80)
        print("SDLC PHASE 2: DESIGN")
        print("=" * 80)

        design = {
            "architecture": {
                "parallel_processing": True,
                "worker_count": get_optimal_worker_count(),
                "batch_size": 100,
                "validation_enabled": True
            },
            "data_flow": [
                "research/ → Clean → Normalize → Validate → data/processed/",
                "research/ → Transform → Aggregate → data/cleaned/"
            ],
            "processing_steps": [
                "1. Scan and catalog all research files",
                "2. Clean JSON structure and syntax",
                "3. Normalize state/jurisdiction references",
                "4. Validate data consistency",
                "5. Transform to data/ directory structure",
                "6. Generate quality reports"
            ],
            "output_structure": {
                "processed": "data/processed/",
                "cleaned": "data/cleaned/",
                "reports": "data/processed/reports/"
            }
        }

        print("\n  Architecture:")
        print(f"    - Parallel processing: {design['architecture']['parallel_processing']}")
        print(f"    - Worker processes: {design['architecture']['worker_count']}")
        print(f"    - Batch size: {design['architecture']['batch_size']}")

        print("\n  Data Flow:")
        for flow in design["data_flow"]:
            print(f"    {flow}")

        print("\n  Processing Steps:")
        for step in design["processing_steps"]:
            print(f"    {step}")

        self.results["phase2_design"] = design
        return design

    # ============================================================================
    # PHASE 3: IMPLEMENTATION
    # ============================================================================

    def phase3_implementation(self, design: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Implement data processing pipeline."""
        print("\n" + "=" * 80)
        print("SDLC PHASE 3: IMPLEMENTATION")
        print("=" * 80)

        implementation = {
            "files_processed": 0,
            "files_cleaned": 0,
            "files_normalized": 0,
            "files_transformed": 0,
            "errors": [],
            "start_time": datetime.now().isoformat()
        }

        # Get all JSON files
        json_files = list(RESEARCH_DIR.rglob('*.json'))
        total_files = len(json_files)

        print(f"\nProcessing {total_files} research files...")

        # Process files in parallel
        worker_count = design["architecture"]["worker_count"]
        batch_size = design["architecture"]["batch_size"]

        with ProcessPoolExecutor(max_workers=worker_count) as executor:
            # Submit batches
            futures = []
            for i in range(0, total_files, batch_size):
                batch = json_files[i:i + batch_size]
                for json_file in batch:
                    future = executor.submit(self._process_research_file, json_file)
                    futures.append((future, json_file))

            # Process results
            for future, json_file in futures:
                try:
                    result = future.result()
                    implementation["files_processed"] += 1

                    if result["cleaned"]:
                        implementation["files_cleaned"] += 1
                    if result["normalized"]:
                        implementation["files_normalized"] += 1
                    if result["transformed"]:
                        implementation["files_transformed"] += 1

                    if result["error"]:
                        implementation["errors"].append({
                            "file": str(json_file),
                            "error": result["error"]
                        })

                    if implementation["files_processed"] % 100 == 0:
                        print(f"  Processed {implementation['files_processed']}/{total_files} files...")

                except Exception as e:
                    implementation["errors"].append({
                        "file": str(json_file),
                        "error": str(e)
                    })

        implementation["end_time"] = datetime.now().isoformat()
        implementation["elapsed_seconds"] = (
            datetime.fromisoformat(implementation["end_time"]) -
            datetime.fromisoformat(implementation["start_time"])
        ).total_seconds()

        print(f"\n  Files processed: {implementation['files_processed']}")
        print(f"  Files cleaned: {implementation['files_cleaned']}")
        print(f"  Files normalized: {implementation['files_normalized']}")
        print(f"  Files transformed: {implementation['files_transformed']}")
        print(f"  Errors: {len(implementation['errors'])}")
        print(f"  Elapsed time: {implementation['elapsed_seconds']:.2f} seconds")

        self.results["phase3_implementation"] = implementation
        return implementation

    def _process_research_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single research file."""
        result = {
            "cleaned": False,
            "normalized": False,
            "transformed": False,
            "error": None
        }

        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Clean and normalize
            original_data = json.dumps(data, sort_keys=True)
            cleaned_data = normalize_dict_recursive(data)
            normalized_data = json.dumps(cleaned_data, sort_keys=True)

            # Always write cleaned version to data/cleaned/ (even if no changes)
            # This ensures all research data is available in cleaned format
            rel_path = file_path.relative_to(RESEARCH_DIR)
            output_path = DATA_CLEANED_DIR / rel_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

            result["transformed"] = True

            # Check if changes were made
            if original_data != normalized_data:
                result["cleaned"] = True
                result["normalized"] = True

        except Exception as e:
            result["error"] = str(e)

        return result

    # ============================================================================
    # PHASE 4: TESTING
    # ============================================================================

    def phase4_testing(self, implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 4: Test processed data quality."""
        print("\n" + "=" * 80)
        print("SDLC PHASE 4: TESTING")
        print("=" * 80)

        testing = {
            "files_tested": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": []
        }

        # Test cleaned files
        cleaned_files = list(DATA_CLEANED_DIR.rglob('*.json'))

        print(f"\nTesting {len(cleaned_files)} cleaned files...")

        for cleaned_file in cleaned_files:
            testing["files_tested"] += 1

            test_result = self._test_file_quality(cleaned_file)
            testing["test_results"].append(test_result)

            if test_result["passed"]:
                testing["tests_passed"] += 1
            else:
                testing["tests_failed"] += 1

        print(f"\n  Tests passed: {testing['tests_passed']}")
        print(f"  Tests failed: {testing['tests_failed']}")
        print(f"  Success rate: {testing['tests_passed'] / testing['files_tested'] * 100:.1f}%")

        self.results["phase4_testing"] = testing
        return testing

    def _test_file_quality(self, file_path: Path) -> Dict[str, Any]:
        """Test quality of a processed file."""
        result = {
            "file": str(file_path),
            "passed": False,
            "issues": []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Test 1: Valid JSON
            if not isinstance(data, (dict, list)):
                result["issues"].append("Invalid JSON structure")

            # Test 2: No unnormalized state references
            data_str = json.dumps(data)
            if 'district_of_columbia' in data_str:
                result["issues"].append("Contains unnormalized 'district_of_columbia'")

            # Test 3: No uppercase state codes in keys
            if isinstance(data, dict):
                for key in data.keys():
                    if isinstance(key, str) and len(key) == 2 and key.isupper() and key.isalpha():
                        result["issues"].append(f"Uppercase state code in key: {key}")

            result["passed"] = len(result["issues"]) == 0

        except Exception as e:
            result["issues"].append(f"Error reading file: {str(e)}")

        return result

    # ============================================================================
    # PHASE 5: DEPLOYMENT
    # ============================================================================

    def phase5_deployment(self, testing: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 5: Deploy processed data to data/ directory."""
        print("\n" + "=" * 80)
        print("SDLC PHASE 5: DEPLOYMENT")
        print("=" * 80)

        deployment = {
            "files_deployed": 0,
            "aggregated_datasets": {},
            "reports_generated": []
        }

        # Aggregate data by category
        print("\nAggregating data by category...")

        cleaned_files = list(DATA_CLEANED_DIR.rglob('*.json'))

        categories = {}
        for cleaned_file in cleaned_files:
            rel_path = cleaned_file.relative_to(DATA_CLEANED_DIR)
            category = str(rel_path).split('/')[0] if '/' in str(rel_path) else "root"

            if category not in categories:
                categories[category] = []

            try:
                with open(cleaned_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                categories[category].append(data)
            except:
                pass

        # Create aggregated datasets
        for category, data_list in categories.items():
            if data_list:
                output_file = DATA_PROCESSED_DIR / f"research_{category}_aggregated.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "category": category,
                        "count": len(data_list),
                        "data": data_list,
                        "processed_date": datetime.now().isoformat()
                    }, f, indent=2, ensure_ascii=False)

                deployment["aggregated_datasets"][category] = len(data_list)
                deployment["files_deployed"] += 1

        print(f"\n  Aggregated datasets created: {len(deployment['aggregated_datasets'])}")
        for category, count in deployment["aggregated_datasets"].items():
            print(f"    - {category}: {count} items")

        self.results["phase5_deployment"] = deployment
        return deployment

    # ============================================================================
    # PHASE 6: VALIDATION & MAINTENANCE
    # ============================================================================

    def phase6_validation(self) -> Dict[str, Any]:
        """Phase 6: Final validation and quality assurance."""
        print("\n" + "=" * 80)
        print("SDLC PHASE 6: VALIDATION & MAINTENANCE")
        print("=" * 80)

        validation = {
            "overall_status": "pending",
            "data_quality_score": 0.0,
            "completeness_score": 0.0,
            "consistency_score": 0.0,
            "recommendations": []
        }

        # Calculate scores
        total_phases = 6
        completed_phases = sum(1 for phase in [
            self.results.get("phase1_requirements"),
            self.results.get("phase2_design"),
            self.results.get("phase3_implementation"),
            self.results.get("phase4_testing"),
            self.results.get("phase5_deployment"),
            self.results.get("phase6_validation")
        ] if phase)

        validation["completeness_score"] = (completed_phases / total_phases) * 100

        # Data quality score
        if self.results.get("phase4_testing"):
            testing = self.results["phase4_testing"]
            if testing.get("files_tested", 0) > 0:
                validation["data_quality_score"] = (
                    testing.get("tests_passed", 0) / testing.get("files_tested", 1)
                ) * 100

        # Consistency score
        if self.results.get("phase3_implementation"):
            impl = self.results["phase3_implementation"]
            if impl.get("files_processed", 0) > 0:
                error_rate = len(impl.get("errors", [])) / impl.get("files_processed", 1)
                validation["consistency_score"] = (1 - error_rate) * 100

        # Overall status
        if validation["data_quality_score"] >= 95 and \
           validation["completeness_score"] == 100:
            validation["overall_status"] = "success"
        elif validation["data_quality_score"] >= 80:
            validation["overall_status"] = "acceptable"
        else:
            validation["overall_status"] = "needs_improvement"

        # Recommendations
        if validation["data_quality_score"] < 95:
            validation["recommendations"].append(
                "Review and fix data quality issues in processed files"
            )
        if validation["consistency_score"] < 95:
            validation["recommendations"].append(
                "Address consistency issues in data processing"
            )

        print(f"\n  Overall Status: {validation['overall_status'].upper()}")
        print(f"  Data Quality Score: {validation['data_quality_score']:.1f}%")
        print(f"  Completeness Score: {validation['completeness_score']:.1f}%")
        print(f"  Consistency Score: {validation['consistency_score']:.1f}%")

        if validation["recommendations"]:
            print("\n  Recommendations:")
            for rec in validation["recommendations"]:
                print(f"    - {rec}")

        self.results["phase6_validation"] = validation
        return validation

    # ============================================================================
    # MAIN EXECUTION
    # ============================================================================

    def run_full_pipeline(self) -> Dict[str, Any]:
        """Run complete SDLC pipeline."""
        print("=" * 80)
        print("SDLC RESEARCH DATA PROCESSING PIPELINE")
        print("=" * 80)
        print(f"Start Time: {self.results['metadata']['start_time']}")
        print()

        try:
            # Phase 1: Requirements Analysis
            requirements = self.phase1_requirements_analysis()

            # Phase 2: Design
            design = self.phase2_design(requirements)

            # Phase 3: Implementation
            implementation = self.phase3_implementation(design)

            # Phase 4: Testing
            testing = self.phase4_testing(implementation)

            # Phase 5: Deployment
            deployment = self.phase5_deployment(testing)

            # Phase 6: Validation
            validation = self.phase6_validation()

            # Generate final report
            self.results["metadata"]["end_time"] = datetime.now().isoformat()
            self.results["metadata"]["status"] = validation["overall_status"]

            # Save results
            report_path = DATA_PROCESSED_DIR / "sdlc_pipeline_report.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)

            print("\n" + "=" * 80)
            print("PIPELINE COMPLETE")
            print("=" * 80)
            print(f"Report saved to: {report_path}")
            print(f"Status: {validation['overall_status'].upper()}")
            print("=" * 80)

            return self.results

        except Exception as e:
            print(f"\nERROR: Pipeline failed - {str(e)}")
            self.results["metadata"]["error"] = str(e)
            self.results["metadata"]["status"] = "failed"
            raise


def main():
    """Main execution."""
    pipeline = SDLCResearchDataPipeline()
    results = pipeline.run_full_pipeline()

    # Exit with appropriate code
    if results["metadata"].get("status") == "success":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
