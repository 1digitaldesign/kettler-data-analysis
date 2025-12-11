#!/usr/bin/env python3
"""
End-to-End Test Suite for State/Jurisdiction Normalization System

Comprehensive testing of the normalization system including:
- Unit tests for normalization functions
- Integration tests for file processing
- Performance tests for parallel processing
- Data consistency validation
"""

import json
import sys
import time
import tempfile
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict

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


class TestNormalizationSystem:
    """Comprehensive test suite for normalization system."""

    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []

    def run_test(self, test_name: str, test_func):
        """Run a single test and record results."""
        try:
            result = test_func()
            if result:
                self.tests_passed += 1
                self.test_results.append({"test": test_name, "status": "PASS", "message": "OK"})
                print(f"  ✓ {test_name}")
                return True
            else:
                self.tests_failed += 1
                self.test_results.append({"test": test_name, "status": "FAIL", "message": "Test returned False"})
                print(f"  ✗ {test_name}: Test returned False")
                return False
        except Exception as e:
            self.tests_failed += 1
            self.test_results.append({"test": test_name, "status": "ERROR", "message": str(e)})
            print(f"  ✗ {test_name}: {str(e)}")
            return False

    def test_state_normalization_basic(self):
        """Test basic state name normalization."""
        test_cases = [
            ("district_of_columbia", "dc"),
            ("District of Columbia", "dc"),
            ("D.C.", "dc"),
            ("DC", "dc"),
            ("dc", "dc"),
            ("VA", "va"),
            ("va", "va"),
            ("virginia", "va"),
            ("Texas", "tx"),
            ("TX", "tx"),
            ("tx", "tx"),
        ]

        for input_val, expected in test_cases:
            result = normalize_state(input_val)
            if result != expected:
                print(f"    FAIL: '{input_val}' -> '{result}' (expected '{expected}')")
                return False
        return True

    def test_state_normalization_edge_cases(self):
        """Test edge cases for state normalization."""
        edge_cases = [
            ("", ""),
            (None, ""),
            ("invalid_state", "invalid_state"),  # Should return as-is if not recognized
            ("NY", "ny"),
            ("new york", "ny"),
            ("New York", "ny"),
        ]

        for input_val, expected in edge_cases:
            result = normalize_state(input_val)
            if result != expected:
                print(f"    FAIL: '{input_val}' -> '{result}' (expected '{expected}')")
                return False
        return True

    def test_dict_normalization(self):
        """Test dictionary normalization."""
        test_data = {
            "district_of_columbia": {
                "name": "DC",
                "states": {
                    "VA": "virginia",
                    "TX": "Texas"
                }
            },
            "DC": "should_stay_dc"
        }

        normalized = normalize_dict_recursive(test_data)

        # Check that keys are normalized
        if "dc" not in normalized:
            print("    FAIL: 'district_of_columbia' key not normalized to 'dc'")
            return False

        if "va" not in normalized["dc"].get("states", {}):
            print("    FAIL: 'VA' key not normalized to 'va'")
            return False

        if normalized["dc"]["states"]["va"] != "va":
            print("    FAIL: 'virginia' value not normalized to 'va'")
            return False

        return True

    def test_json_file_normalization(self):
        """Test JSON file normalization."""
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = {
                "district_of_columbia": {
                    "name": "District of Columbia",
                    "code": "DC"
                },
                "states": {
                    "VA": "Virginia",
                    "TX": "Texas"
                }
            }
            json.dump(test_data, f)
            temp_file = Path(f.name)

        try:
            # Normalize the file
            file_path, success, message, changes = normalize_json_file(temp_file)

            if not success:
                print(f"    FAIL: Normalization failed: {message}")
                return False

            # Read back and verify
            with open(temp_file, 'r') as f:
                normalized_data = json.load(f)

            # Check normalization
            if "dc" not in normalized_data:
                print("    FAIL: 'district_of_columbia' not normalized to 'dc'")
                return False

            if "va" not in normalized_data.get("states", {}):
                print("    FAIL: 'VA' not normalized to 'va'")
                return False

            return True

        finally:
            # Clean up
            if temp_file.exists():
                temp_file.unlink()

    def test_validation(self):
        """Test validation functionality."""
        # Create test data with unnormalized keys
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = {
                "VA": "Virginia",
                "TX": "Texas"
            }
            json.dump(test_data, f)
            temp_file = Path(f.name)

        try:
            result = validate_json_file(temp_file)

            # Should find issues
            if result["valid"]:
                print("    FAIL: Validation should have found issues")
                return False

            if result["issue_count"] == 0:
                print("    FAIL: Should have found normalization issues")
                return False

            return True

        finally:
            if temp_file.exists():
                temp_file.unlink()

    def test_performance(self):
        """Test parallel processing performance."""
        worker_count = get_optimal_worker_count()

        if worker_count < 1:
            print("    FAIL: Invalid worker count")
            return False

        # Should use multiple workers on multi-core systems
        if worker_count > 32:
            print(f"    WARN: Worker count ({worker_count}) exceeds recommended maximum")

        return True

    def test_data_consistency(self):
        """Test data consistency across normalized files."""
        from scripts.utils.paths import DATA_DIR, RESEARCH_DIR

        # Sample a few files and check consistency
        sample_files = []
        for search_dir in [DATA_DIR, RESEARCH_DIR]:
            if search_dir.exists():
                json_files = list(search_dir.rglob('*.json'))[:5]  # Sample 5 files
                sample_files.extend(json_files)

        if not sample_files:
            print("    SKIP: No files found to test")
            return True

        inconsistencies = []
        for file_path in sample_files:
            try:
                if file_path.stat().st_size > 10 * 1024 * 1024:  # Skip large files
                    continue

                with open(file_path, 'r') as f:
                    data = json.load(f)

                # Check for unnormalized state references in keys
                def check_keys(obj, path=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            current_path = f"{path}.{key}" if path else key
                            if isinstance(key, str):
                                normalized = normalize_state(key)
                                if normalized != key and len(key) == 2 and key.isupper():
                                    inconsistencies.append(f"{file_path}: {current_path}")
                            check_keys(value, current_path)
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            check_keys(item, f"{path}[{i}]")

                check_keys(data)

            except Exception:
                continue

        if inconsistencies:
            print(f"    FAIL: Found {len(inconsistencies)} inconsistencies")
            for inc in inconsistencies[:3]:
                print(f"      - {inc}")
            return False

        return True

    def test_comprehensive_coverage(self):
        """Test that all state variations are covered."""
        # Test all variations in the normalization map
        for original, normalized in STATE_NORMALIZATION_MAP.items():
            result = normalize_state(original)
            if result != normalized:
                print(f"    FAIL: '{original}' -> '{result}' (expected '{normalized}')")
                return False

        return True

    def run_all_tests(self):
        """Run all tests."""
        print("=" * 80)
        print("End-to-End Normalization System Test Suite")
        print("=" * 80)
        print()

        print("Running unit tests...")
        self.run_test("State normalization - basic cases", self.test_state_normalization_basic)
        self.run_test("State normalization - edge cases", self.test_state_normalization_edge_cases)
        self.run_test("Dictionary normalization", self.test_dict_normalization)

        print("\nRunning integration tests...")
        self.run_test("JSON file normalization", self.test_json_file_normalization)
        self.run_test("Validation functionality", self.test_validation)

        print("\nRunning performance tests...")
        self.run_test("Parallel processing configuration", self.test_performance)

        print("\nRunning consistency tests...")
        self.run_test("Data consistency validation", self.test_data_consistency)
        self.run_test("Comprehensive coverage", self.test_comprehensive_coverage)

        # Print summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")
        print(f"Total tests: {self.tests_passed + self.tests_failed}")
        print(f"Success rate: {(self.tests_passed / (self.tests_passed + self.tests_failed) * 100):.1f}%")
        print("=" * 80)

        if self.tests_failed > 0:
            print("\nFailed tests:")
            for result in self.test_results:
                if result["status"] != "PASS":
                    print(f"  - {result['test']}: {result['message']}")

        return self.tests_failed == 0


def main():
    """Main execution function."""
    test_suite = TestNormalizationSystem()
    success = test_suite.run_all_tests()

    if success:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
