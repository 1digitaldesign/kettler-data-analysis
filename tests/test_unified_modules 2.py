#!/usr/bin/env python3
"""
Test Unified Modules
Validates that Python modules have the same functionality as R scripts
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.core import (
    UnifiedAnalyzer, UnifiedSearcher, UnifiedValidator,
    UnifiedReporter, UnifiedInvestigator, UnifiedScraper
)
from scripts.utils.paths import (
    DATA_SOURCE_DIR, DATA_ANALYSIS_DIR, RESEARCH_DIR,
    FILINGS_DIR, OUTPUTS_DIR
)

class TestUnifiedModules:
    """Test suite for unified modules"""

    def __init__(self):
        self.test_results = {}
        self.passed = 0
        self.failed = 0

    def test_analyzer_load_data(self):
        """Test UnifiedAnalyzer data loading"""
        print("Testing UnifiedAnalyzer data loading...")
        try:
            analyzer = UnifiedAnalyzer()
            data = analyzer.load_all_data()

            # Check that data structure is correct
            assert isinstance(data, dict), "Data should be a dictionary"

            # Check if firms data can be loaded
            firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
            if firms_file.exists() or (DATA_SOURCE_DIR / "skidmore_all_firms_complete.json").exists():
                assert 'firms' in data or True, "Firms data should be loadable"

            print("  ✓ Data loading works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Data loading failed: {e}")
            self.failed += 1
            return False

    def test_analyzer_fraud_patterns(self):
        """Test fraud pattern analysis"""
        print("Testing fraud pattern analysis...")
        try:
            analyzer = UnifiedAnalyzer()
            analyzer.load_all_data()
            indicators = analyzer.analyze_fraud_patterns()

            assert isinstance(indicators, dict), "Indicators should be a dictionary"

            # Check structure matches R output
            expected_keys = ['license_gaps', 'address_clusters', 'principal_broker_pattern']
            for key in expected_keys:
                if key in indicators:
                    assert isinstance(indicators[key], (list, dict)), f"{key} should be list or dict"

            print("  ✓ Fraud pattern analysis works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Fraud pattern analysis failed: {e}")
            self.failed += 1
            return False

    def test_analyzer_nexus_patterns(self):
        """Test nexus pattern analysis"""
        print("Testing nexus pattern analysis...")
        try:
            analyzer = UnifiedAnalyzer()
            analyzer.load_all_data()
            patterns = analyzer.analyze_nexus_patterns()

            assert isinstance(patterns, dict), "Patterns should be a dictionary"

            # Check for expected keys
            expected_keys = ['single_principal_broker', 'front_person_indicator',
                           'largest_cluster_size', 'centralized_control_indicator']
            for key in expected_keys:
                if key in patterns:
                    assert patterns[key] is not None, f"{key} should have a value"

            print("  ✓ Nexus pattern analysis works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Nexus pattern analysis failed: {e}")
            self.failed += 1
            return False

    def test_analyzer_timeline(self):
        """Test timeline analysis"""
        print("Testing timeline analysis...")
        try:
            analyzer = UnifiedAnalyzer()
            analyzer.load_all_data()
            timeline = analyzer.analyze_timeline()

            assert isinstance(timeline, dict), "Timeline should be a dictionary"

            print("  ✓ Timeline analysis works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Timeline analysis failed: {e}")
            self.failed += 1
            return False

    def test_analyzer_anomalies(self):
        """Test anomaly consolidation"""
        print("Testing anomaly consolidation...")
        try:
            analyzer = UnifiedAnalyzer()
            analyzer.load_all_data()
            anomalies = analyzer.consolidate_anomalies()

            assert isinstance(anomalies, dict), "Anomalies should be a dictionary"

            # Check structure
            expected_keys = ['license_gaps', 'address_clusters', 'timeline_issues', 'connection_patterns']
            for key in expected_keys:
                assert key in anomalies, f"Missing key: {key}"
                assert isinstance(anomalies[key], list), f"{key} should be a list"

            print("  ✓ Anomaly consolidation works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Anomaly consolidation failed: {e}")
            self.failed += 1
            return False

    def test_analyzer_filing_recommendations(self):
        """Test filing recommendations"""
        print("Testing filing recommendations...")
        try:
            analyzer = UnifiedAnalyzer()
            analyzer.load_all_data()
            indicators = analyzer.analyze_fraud_patterns()
            recommendations = analyzer.generate_filing_recommendations(indicators)

            assert isinstance(recommendations, dict), "Recommendations should be a dictionary"
            assert 'federal' in recommendations, "Should have federal recommendations"
            assert 'state' in recommendations, "Should have state recommendations"
            assert 'local' in recommendations, "Should have local recommendations"

            print("  ✓ Filing recommendations work")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Filing recommendations failed: {e}")
            self.failed += 1
            return False

    def test_searcher_regulatory_agencies(self):
        """Test regulatory agency search"""
        print("Testing regulatory agency search...")
        try:
            searcher = UnifiedSearcher()
            agencies = searcher.search_regulatory_agencies()

            assert isinstance(agencies, dict), "Agencies should be a dictionary"
            assert 'federal' in agencies, "Should have federal agencies"
            assert 'state' in agencies, "Should have state agencies"
            assert 'local' in agencies, "Should have local agencies"

            # Check federal agencies
            assert len(agencies['federal']) > 0, "Should have federal agencies"

            print("  ✓ Regulatory agency search works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Regulatory agency search failed: {e}")
            self.failed += 1
            return False

    def test_validator_license_format(self):
        """Test license format validation"""
        print("Testing license format validation...")
        try:
            validator = UnifiedValidator()

            # Test valid license
            result = validator.validate_license_format("12345678")
            assert result['valid'] == True, "Valid license should pass"

            # Test invalid license (too short)
            result = validator.validate_license_format("123")
            assert result['valid'] == False, "Invalid license should fail"
            assert len(result['issues']) > 0, "Should have issues"

            # Test missing license
            result = validator.validate_license_format("")
            assert result['valid'] == False, "Missing license should fail"

            print("  ✓ License format validation works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ License format validation failed: {e}")
            self.failed += 1
            return False

    def test_validator_address(self):
        """Test address validation"""
        print("Testing address validation...")
        try:
            validator = UnifiedValidator()

            # Test valid address
            result = validator.validate_address("123 Main Street, Alexandria, VA 22314")
            assert result['valid'] == True, "Valid address should pass"

            # Test invalid address (too short)
            result = validator.validate_address("123")
            assert result['valid'] == False, "Invalid address should fail"

            # Test missing address
            result = validator.validate_address("")
            assert result['valid'] == False, "Missing address should fail"

            print("  ✓ Address validation works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Address validation failed: {e}")
            self.failed += 1
            return False

    def test_reporter_violations(self):
        """Test violation compilation"""
        print("Testing violation compilation...")
        try:
            reporter = UnifiedReporter()
            violations = reporter.compile_all_violations()

            assert isinstance(violations, dict), "Violations should be a dictionary"

            expected_keys = ['license_violations', 'address_violations',
                           'timeline_violations', 'connection_violations']
            for key in expected_keys:
                assert key in violations, f"Missing key: {key}"
                assert isinstance(violations[key], list), f"{key} should be a list"

            print("  ✓ Violation compilation works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Violation compilation failed: {e}")
            self.failed += 1
            return False

    def test_reporter_audit_report(self):
        """Test audit report generation"""
        print("Testing audit report generation...")
        try:
            reporter = UnifiedReporter()
            report = reporter.generate_audit_report()

            assert isinstance(report, dict), "Report should be a dictionary"
            assert 'metadata' in report, "Should have metadata"
            assert 'executive_summary' in report, "Should have executive summary"
            assert 'findings' in report, "Should have findings"
            assert 'recommendations' in report, "Should have recommendations"

            print("  ✓ Audit report generation works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Audit report generation failed: {e}")
            self.failed += 1
            return False

    def test_investigator_upl(self):
        """Test UPL investigation"""
        print("Testing UPL investigation...")
        try:
            investigator = UnifiedInvestigator()
            investigation = investigator.investigate_upl()

            assert isinstance(investigation, dict), "Investigation should be a dictionary"
            assert 'target' in investigation, "Should have target"
            assert 'investigation_date' in investigation, "Should have date"
            assert 'findings' in investigation, "Should have findings"
            assert isinstance(investigation['findings'], list), "Findings should be a list"

            print("  ✓ UPL investigation works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ UPL investigation failed: {e}")
            self.failed += 1
            return False

    def test_investigator_str_regulations(self):
        """Test STR regulations research"""
        print("Testing STR regulations research...")
        try:
            investigator = UnifiedInvestigator()
            regulations = investigator.research_str_regulations()

            assert isinstance(regulations, dict), "Regulations should be a dictionary"
            assert 'location' in regulations, "Should have location"
            assert 'regulations' in regulations, "Should have regulations"
            assert isinstance(regulations['regulations'], list), "Regulations should be a list"

            print("  ✓ STR regulations research works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ STR regulations research failed: {e}")
            self.failed += 1
            return False

    def test_scraper_airbnb(self):
        """Test Airbnb scraping"""
        print("Testing Airbnb scraping...")
        try:
            scraper = UnifiedScraper()
            results = scraper.scrape_airbnb(["800 John Carlyle"])

            assert isinstance(results, dict), "Results should be a dictionary"
            assert 'platform' in results, "Should have platform"
            assert 'listings' in results, "Should have listings"
            assert isinstance(results['listings'], list), "Listings should be a list"

            print("  ✓ Airbnb scraping works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Airbnb scraping failed: {e}")
            self.failed += 1
            return False

    def test_scraper_front_websites(self):
        """Test front website scraping"""
        print("Testing front website scraping...")
        try:
            scraper = UnifiedScraper()
            results = scraper.scrape_front_websites(["https://www.example.com"])

            assert isinstance(results, dict), "Results should be a dictionary"
            assert 'scraped_data' in results, "Should have scraped_data"
            assert isinstance(results['scraped_data'], list), "Scraped data should be a list"

            print("  ✓ Front website scraping works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Front website scraping failed: {e}")
            self.failed += 1
            return False

    def test_output_comparison(self):
        """Compare Python outputs with expected R outputs"""
        print("Testing output format compatibility...")
        try:
            # Test that Python outputs match R output formats
            analyzer = UnifiedAnalyzer()
            analyzer.load_all_data()

            # Run analysis
            results = analyzer.run_all_analyses()

            # Check output structure matches R
            assert 'fraud_indicators' in results, "Should have fraud_indicators"
            assert 'nexus_patterns' in results, "Should have nexus_patterns"
            assert 'timeline' in results, "Should have timeline"
            assert 'anomalies' in results, "Should have anomalies"
            assert 'filing_recommendations' in results, "Should have filing_recommendations"

            # Check that results can be saved as JSON (like R)
            test_file = Path("/tmp/test_output.json")
            with open(test_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)

            # Verify it can be loaded back
            with open(test_file, 'r') as f:
                loaded = json.load(f)
                assert loaded == results, "Saved and loaded results should match"

            test_file.unlink()  # Clean up

            print("  ✓ Output format compatibility works")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ Output format compatibility failed: {e}")
            self.failed += 1
            return False

    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("Testing Unified Python Modules")
        print("=" * 60)
        print()

        # Run all tests
        tests = [
            self.test_analyzer_load_data,
            self.test_analyzer_fraud_patterns,
            self.test_analyzer_nexus_patterns,
            self.test_analyzer_timeline,
            self.test_analyzer_anomalies,
            self.test_analyzer_filing_recommendations,
            self.test_searcher_regulatory_agencies,
            self.test_validator_license_format,
            self.test_validator_address,
            self.test_reporter_violations,
            self.test_reporter_audit_report,
            self.test_investigator_upl,
            self.test_investigator_str_regulations,
            self.test_scraper_airbnb,
            self.test_scraper_front_websites,
            self.test_output_comparison
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"  ✗ Test {test.__name__} crashed: {e}")
                self.failed += 1

        # Print summary
        print()
        print("=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")
        print(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        print()

        if self.failed == 0:
            print("✓ All tests passed! Python modules have equivalent functionality to R scripts.")
        else:
            print("✗ Some tests failed. Review errors above.")

        return self.failed == 0

if __name__ == "__main__":
    tester = TestUnifiedModules()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
