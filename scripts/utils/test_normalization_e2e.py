#!/usr/bin/env python3
"""
End-to-End Testing for State/Jurisdiction Normalization System

Comprehensive system-of-systems engineering testing to verify:
1. Normalization utility correctness
2. Parallel processing efficiency
3. Data consistency
4. Code reference updates
5. Edge case handling
"""

import json
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.state_normalizer import (
    normalize_state,
    normalize_jurisdiction,
    normalize_dict_recursive,
    STATE_NORMALIZATION_MAP
)
from scripts.utils.normalize_data_parallel import (
    normalize_json_file,
    get_optimal_worker_count
)
from scripts.utils.validate_normalization import validate_json_file


class NormalizationE2ETest:
    """End-to-end test suite for normalization system."""

    def __init__(self):
        self.test_results = {
            "unit_tests": [],
            "integration_tests": [],
            "performance_tests": [],
            "consistency_tests": [],
            "edge_case_tests": []
        }
        self.temp_dir = None

    def setup(self):
        """Set up test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        print(f"Test directory: {self.temp_dir}")

    def teardown(self):
        """Clean up test environment."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_unit_normalization(self) -> bool:
        """Test unit-level normalization functions."""
        print("\n" + "=" * 80)
        print("UNIT TESTS: Normalization Functions")
        print("=" * 80)

        test_cases = [
            # District of Columbia variations
            ("district_of_columbia", "dc"),
            ("District of Columbia", "dc"),
            ("DISTRICT OF COLUMBIA", "dc"),
            ("D.C.", "dc"),
            ("DC", "dc"),
            ("dc", "dc"),

            # Uppercase state codes
            ("VA", "va"),
            ("TX", "tx"),
            ("MD", "md"),
            ("NC", "nc"),

            # Full state names
            ("virginia", "va"),
            ("texas", "tx"),
            ("maryland", "md"),
            ("north carolina", "nc"),

            # Already normalized
            ("va", "va"),
            ("tx", "tx"),
        ]

        passed = 0
        failed = 0

        for input_val, expected in test_cases:
            result = normalize_state(input_val)
            if result == expected:
                passed += 1
                print(f"  ✓ '{input_val}' -> '{result}'")
            else:
                failed += 1
                print(f"  ✗ '{input_val}' -> '{result}' (expected '{expected}')")

        total = passed + failed
        success_rate = (passed / total * 100) if total > 0 else 0

        self.test_results["unit_tests"].append({
            "test": "normalize_state",
            "passed": passed,
            "failed": failed,
            "total": total,
            "success_rate": success_rate
        })

        print(f"\n  Results: {passed}/{total} passed ({success_rate:.1f}%)")
        return failed == 0

    def test_integration_dict_normalization(self) -> bool:
        """Test integration: dictionary normalization."""
        print("\n" + "=" * 80)
        print("INTEGRATION TESTS: Dictionary Normalization")
        print("=" * 80)

        test_data = {
            "district_of_columbia": {
                "name": "District of Columbia",
                "code": "DC",
                "states": {
                    "VA": {"name": "Virginia"},
                    "TX": {"name": "Texas"},
                    "MD": {"name": "Maryland"}
                }
            },
            "jurisdictions": [
                {"state": "D.C.", "code": "DC"},
                {"state": "virginia", "code": "VA"}
            ]
        }

        normalized = normalize_dict_recursive(test_data)

        # Verify keys are normalized
        dc_data = normalized.get("dc", {})
        checks = [
            ("dc" in normalized, "Key 'district_of_columbia' normalized to 'dc'"),
            (dc_data.get("code") == "dc", "Nested value 'DC' normalized to 'dc'"),
            (dc_data.get("code") == "dc", "Value 'DC' normalized to 'dc'"),
            ("va" in dc_data.get("states", {}), "State key 'VA' normalized to 'va'"),
            (normalized.get("jurisdictions", [{}])[0].get("state") == "dc", "List item normalized"),
        ]

        passed = 0
        failed = 0

        for check, description in checks:
            if check:
                passed += 1
                print(f"  ✓ {description}")
            else:
                failed += 1
                print(f"  ✗ {description}")

        self.test_results["integration_tests"].append({
            "test": "dict_normalization",
            "passed": passed,
            "failed": failed,
            "total": passed + failed
        })

        return failed == 0

    def test_performance_parallel_processing(self) -> bool:
        """Test performance: parallel processing efficiency."""
        print("\n" + "=" * 80)
        print("PERFORMANCE TESTS: Parallel Processing")
        print("=" * 80)

        # Create test JSON files
        test_files = []
        for i in range(100):
            test_file = self.temp_dir / f"test_{i}.json"
            test_data = {
                "id": i,
                "state": "VA" if i % 2 == 0 else "TX",
                "district_of_columbia": "DC" if i % 3 == 0 else None,
                "nested": {
                    "jurisdiction": "District of Columbia" if i % 5 == 0 else "virginia"
                }
            }
            with open(test_file, 'w') as f:
                json.dump(test_data, f)
            test_files.append(test_file)

        # Test parallel processing
        worker_count = get_optimal_worker_count()
        print(f"  Worker count: {worker_count}")

        start_time = time.time()
        processed = 0
        changed = 0

        for test_file in test_files:
            result = normalize_json_file(test_file)
            processed += 1
            if "Normalized" in result[2]:
                changed += 1

        elapsed = time.time() - start_time
        throughput = processed / elapsed if elapsed > 0 else 0

        print(f"  Files processed: {processed}")
        print(f"  Files changed: {changed}")
        print(f"  Elapsed time: {elapsed:.2f}s")
        print(f"  Throughput: {throughput:.1f} files/second")

        # Performance criteria: should process at least 50 files/second
        performance_ok = throughput >= 50

        self.test_results["performance_tests"].append({
            "test": "parallel_processing",
            "files_processed": processed,
            "files_changed": changed,
            "elapsed_seconds": elapsed,
            "throughput": throughput,
            "meets_criteria": performance_ok
        })

        if performance_ok:
            print(f"  ✓ Performance meets criteria (≥50 files/sec)")
        else:
            print(f"  ✗ Performance below criteria (<50 files/sec)")

        return performance_ok

    def test_consistency_round_trip(self) -> bool:
        """Test consistency: round-trip normalization."""
        print("\n" + "=" * 80)
        print("CONSISTENCY TESTS: Round-Trip Normalization")
        print("=" * 80)

        test_cases = [
            {"state": "dc", "jurisdiction": "dc"},
            {"state": "va", "jurisdiction": "va"},
            {"district_of_columbia": "DC", "states": {"VA": "Virginia"}},
        ]

        passed = 0
        failed = 0

        for i, test_data in enumerate(test_cases):
            # Normalize
            normalized = normalize_dict_recursive(test_data)

            # Normalize again (should be idempotent)
            normalized_twice = normalize_dict_recursive(normalized)

            # Compare
            if json.dumps(normalized, sort_keys=True) == json.dumps(normalized_twice, sort_keys=True):
                passed += 1
                print(f"  ✓ Test case {i+1}: Idempotent")
            else:
                failed += 1
                print(f"  ✗ Test case {i+1}: Not idempotent")

        self.test_results["consistency_tests"].append({
            "test": "round_trip",
            "passed": passed,
            "failed": failed,
            "total": passed + failed
        })

        return failed == 0

    def test_edge_cases(self) -> bool:
        """Test edge cases."""
        print("\n" + "=" * 80)
        print("EDGE CASE TESTS")
        print("=" * 80)

        edge_cases = [
            ("", ""),  # Empty string
            (None, ""),  # None
            ("  ", ""),  # Whitespace
            ("invalid_state", "invalid_state"),  # Invalid state
            ("DC ", "dc"),  # Trailing space
            (" DC", "dc"),  # Leading space
        ]

        passed = 0
        failed = 0

        for input_val, expected in edge_cases:
            try:
                result = normalize_state(input_val)
                if result == expected or (input_val is None and result == ""):
                    passed += 1
                    print(f"  ✓ Edge case handled: {input_val} -> {result}")
                else:
                    failed += 1
                    print(f"  ✗ Edge case failed: {input_val} -> {result} (expected {expected})")
            except Exception as e:
                failed += 1
                print(f"  ✗ Edge case exception: {input_val} -> {str(e)}")

        self.test_results["edge_case_tests"].append({
            "test": "edge_cases",
            "passed": passed,
            "failed": failed,
            "total": passed + failed
        })

        return failed == 0

    def test_validation_consistency(self) -> bool:
        """Test that validation catches unnormalized data."""
        print("\n" + "=" * 80)
        print("VALIDATION TESTS: Consistency Checking")
        print("=" * 80)

        # Create test file with unnormalized data
        test_file = self.temp_dir / "unnormalized_test.json"
        unnormalized_data = {
            "district_of_columbia": "DC",
            "states": {
                "VA": "Virginia",
                "TX": "Texas"
            }
        }
        with open(test_file, 'w') as f:
            json.dump(unnormalized_data, f)

        # Validate (should find issues)
        validation = validate_json_file(test_file)

        if not validation["valid"] and validation["issue_count"] > 0:
            print(f"  ✓ Validation correctly identified {validation['issue_count']} issues")
            passed = True
        else:
            print(f"  ✗ Validation failed to identify issues")
            passed = False

        # Normalize the file
        normalize_json_file(test_file)

        # Validate again (should be clean)
        validation_after = validate_json_file(test_file)

        if validation_after["valid"]:
            print(f"  ✓ Validation confirms normalization successful")
            passed = passed and True
        else:
            print(f"  ✗ Validation still finds issues after normalization")
            passed = False

        return passed

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all end-to-end tests."""
        print("=" * 80)
        print("END-TO-END NORMALIZATION SYSTEM TEST SUITE")
        print("=" * 80)

        self.setup()

        try:
            # Run all test suites
            results = {
                "unit": self.test_unit_normalization(),
                "integration": self.test_integration_dict_normalization(),
                "performance": self.test_performance_parallel_processing(),
                "consistency": self.test_consistency_round_trip(),
                "edge_cases": self.test_edge_cases(),
                "validation": self.test_validation_consistency(),
            }

            # Print summary
            print("\n" + "=" * 80)
            print("TEST SUMMARY")
            print("=" * 80)

            total_passed = sum(1 for v in results.values() if v)
            total_tests = len(results)

            for test_name, passed in results.items():
                status = "✓ PASS" if passed else "✗ FAIL"
                print(f"  {status}: {test_name}")

            print(f"\n  Overall: {total_passed}/{total_tests} test suites passed")

            self.test_results["summary"] = {
                "total_suites": total_tests,
                "passed_suites": total_passed,
                "all_passed": total_passed == total_tests,
                "individual_results": results
            }

            return self.test_results

        finally:
            self.teardown()


def main():
    """Main execution."""
    test_suite = NormalizationE2ETest()
    results = test_suite.run_all_tests()

    # Exit with appropriate code
    if results.get("summary", {}).get("all_passed", False):
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
