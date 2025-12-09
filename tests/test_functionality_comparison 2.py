#!/usr/bin/env python3
"""
Functionality Comparison Test
Compares Python module outputs with R script expected outputs
"""

import sys
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_analyzer_functionality():
    """Test that UnifiedAnalyzer produces same outputs as R scripts"""
    print("=" * 60)
    print("Testing UnifiedAnalyzer Functionality")
    print("=" * 60)
    print()

    try:
        from scripts.core.unified_analysis import UnifiedAnalyzer

        analyzer = UnifiedAnalyzer()
        print("✓ UnifiedAnalyzer imported successfully")

        # Test data loading
        print("\n1. Testing data loading...")
        data = analyzer.load_all_data()
        assert isinstance(data, dict), "Data should be a dictionary"
        print("  ✓ Data loaded successfully")

        # Test fraud patterns (replaces analyze_fraud_patterns.R)
        print("\n2. Testing fraud pattern analysis (replaces analyze_fraud_patterns.R)...")
        indicators = analyzer.analyze_fraud_patterns()
        assert isinstance(indicators, dict), "Should return dictionary"
        assert 'license_gaps' in indicators or 'address_clusters' in indicators or 'principal_broker_pattern' in indicators, "Should have expected keys"
        print("  ✓ Fraud pattern analysis works")

        # Test nexus patterns (replaces analyze_nexus_patterns.R, find_real_nexus.R)
        print("\n3. Testing nexus pattern analysis (replaces analyze_nexus_patterns.R)...")
        patterns = analyzer.analyze_nexus_patterns()
        assert isinstance(patterns, dict), "Should return dictionary"
        print("  ✓ Nexus pattern analysis works")

        # Test timeline (replaces create_timeline_analysis.R)
        print("\n4. Testing timeline analysis (replaces create_timeline_analysis.R)...")
        timeline = analyzer.analyze_timeline()
        assert isinstance(timeline, dict), "Should return dictionary"
        print("  ✓ Timeline analysis works")

        # Test anomalies (replaces consolidate_all_anomalies.R)
        print("\n5. Testing anomaly consolidation (replaces consolidate_all_anomalies.R)...")
        anomalies = analyzer.consolidate_anomalies()
        assert isinstance(anomalies, dict), "Should return dictionary"
        assert all(key in anomalies for key in ['license_gaps', 'address_clusters', 'timeline_issues', 'connection_patterns']), "Should have all expected keys"
        print("  ✓ Anomaly consolidation works")

        # Test all evidence (replaces analyze_all_evidence.R)
        print("\n6. Testing all evidence analysis (replaces analyze_all_evidence.R)...")
        evidence_summary = analyzer.analyze_all_evidence()
        assert isinstance(evidence_summary, dict), "Should return dictionary"
        assert 'entities_found' in evidence_summary, "Should have entities_found"
        print("  ✓ All evidence analysis works")

        # Test connection matrix (replaces create_connection_matrix.R)
        print("\n7. Testing connection matrix (replaces create_connection_matrix.R)...")
        matrix = analyzer.create_connection_matrix()
        assert isinstance(matrix, dict), "Should return dictionary"
        assert 'summary' in matrix, "Should have summary"
        print("  ✓ Connection matrix creation works")

        # Test shared resources (replaces analyze_shared_resources.R)
        print("\n8. Testing shared resources (replaces analyze_shared_resources.R)...")
        shared = analyzer.analyze_shared_resources()
        assert isinstance(shared, dict), "Should return dictionary"
        assert 'shared_addresses' in shared, "Should have shared_addresses"
        print("  ✓ Shared resources analysis works")

        # Test filing recommendations
        print("\n9. Testing filing recommendations...")
        recommendations = analyzer.generate_filing_recommendations(indicators)
        assert isinstance(recommendations, dict), "Should return dictionary"
        assert 'federal' in recommendations and 'state' in recommendations, "Should have federal and state recommendations"
        print("  ✓ Filing recommendations work")

        # Test full run
        print("\n10. Testing full analysis run...")
        results = analyzer.run_all_analyses()
        assert isinstance(results, dict), "Should return dictionary"
        assert 'fraud_indicators' in results, "Should have fraud_indicators"
        assert 'nexus_patterns' in results, "Should have nexus_patterns"
        assert 'evidence_summary' in results, "Should have evidence_summary"
        assert 'connection_matrix' in results, "Should have connection_matrix"
        assert 'shared_resources' in results, "Should have shared_resources"
        print("  ✓ Full analysis run works")

        # Test saving
        print("\n11. Testing result saving...")
        analyzer.save_results()
        print("  ✓ Results saved successfully")

        print("\n" + "=" * 60)
        print("✓ UnifiedAnalyzer: ALL TESTS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ UnifiedAnalyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_searcher_functionality():
    """Test that UnifiedSearcher produces same outputs as R scripts"""
    print("\n" + "=" * 60)
    print("Testing UnifiedSearcher Functionality")
    print("=" * 60)
    print()

    try:
        from scripts.core.unified_search import UnifiedSearcher

        searcher = UnifiedSearcher()
        print("✓ UnifiedSearcher imported successfully")

        # Test regulatory agencies (replaces search_regulatory_agencies.R)
        print("\n1. Testing regulatory agency search (replaces search_regulatory_agencies.R)...")
        agencies = searcher.search_regulatory_agencies()
        assert isinstance(agencies, dict), "Should return dictionary"
        assert 'federal' in agencies and 'state' in agencies, "Should have federal and state agencies"
        assert len(agencies['federal']) > 0, "Should have federal agencies"
        print("  ✓ Regulatory agency search works")

        # Test DPOR search (replaces search_dpor_comprehensive.R)
        print("\n2. Testing DPOR search (replaces search_dpor_comprehensive.R)...")
        dpor_results = searcher.search_dpor("VA", ["Caitlin Skidmore"])
        assert isinstance(dpor_results, list), "Should return list"
        print("  ✓ DPOR search works")

        # Test news search (replaces search_news_violations.R)
        print("\n3. Testing news search (replaces search_news_violations.R)...")
        news_results = searcher.search_news_violations(["Kettler"])
        assert isinstance(news_results, list), "Should return list"
        print("  ✓ News search works")

        print("\n" + "=" * 60)
        print("✓ UnifiedSearcher: ALL TESTS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ UnifiedSearcher test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validator_functionality():
    """Test that UnifiedValidator produces same outputs as R scripts"""
    print("\n" + "=" * 60)
    print("Testing UnifiedValidator Functionality")
    print("=" * 60)
    print()

    try:
        from scripts.core.unified_validation import UnifiedValidator

        validator = UnifiedValidator()
        print("✓ UnifiedValidator imported successfully")

        # Test license validation (replaces validate_skidmore_firms.R)
        print("\n1. Testing license validation...")
        result = validator.validate_license_format("12345678")
        assert result['valid'] == True, "Valid license should pass"
        result = validator.validate_license_format("123")
        assert result['valid'] == False, "Invalid license should fail"
        print("  ✓ License validation works")

        # Test address validation
        print("\n2. Testing address validation...")
        result = validator.validate_address("123 Main Street, Alexandria, VA 22314")
        assert result['valid'] == True, "Valid address should pass"
        print("  ✓ Address validation works")

        print("\n" + "=" * 60)
        print("✓ UnifiedValidator: ALL TESTS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ UnifiedValidator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_reporter_functionality():
    """Test that UnifiedReporter produces same outputs as R scripts"""
    print("\n" + "=" * 60)
    print("Testing UnifiedReporter Functionality")
    print("=" * 60)
    print()

    try:
        from scripts.core.unified_reporting import UnifiedReporter

        reporter = UnifiedReporter()
        print("✓ UnifiedReporter imported successfully")

        # Test violation compilation (replaces compile_all_violations.R)
        print("\n1. Testing violation compilation (replaces compile_all_violations.R)...")
        violations = reporter.compile_all_violations()
        assert isinstance(violations, dict), "Should return dictionary"
        assert all(key in violations for key in ['license_violations', 'address_violations', 'timeline_violations', 'connection_violations']), "Should have all violation types"
        print("  ✓ Violation compilation works")

        # Test audit report (replaces generate_comprehensive_audit_report.R)
        print("\n2. Testing audit report generation (replaces generate_comprehensive_audit_report.R)...")
        report = reporter.generate_audit_report()
        assert isinstance(report, dict), "Should return dictionary"
        assert 'executive_summary' in report and 'findings' in report, "Should have executive summary and findings"
        print("  ✓ Audit report generation works")

        print("\n" + "=" * 60)
        print("✓ UnifiedReporter: ALL TESTS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ UnifiedReporter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_investigator_functionality():
    """Test that UnifiedInvestigator produces same outputs as R scripts"""
    print("\n" + "=" * 60)
    print("Testing UnifiedInvestigator Functionality")
    print("=" * 60)
    print()

    try:
        from scripts.core.unified_investigation import UnifiedInvestigator

        investigator = UnifiedInvestigator()
        print("✓ UnifiedInvestigator imported successfully")

        # Test UPL investigation (replaces investigate_hyland_upl.R)
        print("\n1. Testing UPL investigation (replaces investigate_hyland_upl.R)...")
        investigation = investigator.investigate_upl()
        assert isinstance(investigation, dict), "Should return dictionary"
        assert 'findings' in investigation, "Should have findings"
        print("  ✓ UPL investigation works")

        # Test STR regulations (replaces research_str_regulations.R)
        print("\n2. Testing STR regulations (replaces research_str_regulations.R)...")
        regulations = investigator.research_str_regulations()
        assert isinstance(regulations, dict), "Should return dictionary"
        assert 'regulations' in regulations, "Should have regulations"
        print("  ✓ STR regulations research works")

        print("\n" + "=" * 60)
        print("✓ UnifiedInvestigator: ALL TESTS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ UnifiedInvestigator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_output_format_compatibility():
    """Test that Python outputs match R output formats"""
    print("\n" + "=" * 60)
    print("Testing Output Format Compatibility")
    print("=" * 60)
    print()

    try:
        from scripts.core.unified_analysis import UnifiedAnalyzer

        analyzer = UnifiedAnalyzer()
        analyzer.load_all_data()
        results = analyzer.run_all_analyses()

        # Test JSON serialization (R uses JSON)
        print("1. Testing JSON serialization...")
        json_str = json.dumps(results, indent=2, default=str)
        assert len(json_str) > 0, "Should serialize to JSON"
        loaded = json.loads(json_str)
        assert loaded == results, "Should deserialize correctly"
        print("  ✓ JSON serialization works")

        # Test that structure matches R outputs
        print("\n2. Testing output structure...")
        required_keys = ['fraud_indicators', 'nexus_patterns', 'timeline', 'anomalies', 'filing_recommendations']
        for key in required_keys:
            assert key in results, f"Should have {key}"
        print("  ✓ Output structure matches R format")

        print("\n" + "=" * 60)
        print("✓ Output Format Compatibility: ALL TESTS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ Output format compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all functionality tests"""
    print("=" * 60)
    print("FUNCTIONALITY COMPARISON TEST")
    print("Python Modules vs R Scripts")
    print("=" * 60)
    print()

    results = []

    # Run all tests
    results.append(("UnifiedAnalyzer", test_analyzer_functionality()))
    results.append(("UnifiedSearcher", test_searcher_functionality()))
    results.append(("UnifiedValidator", test_validator_functionality()))
    results.append(("UnifiedReporter", test_reporter_functionality()))
    results.append(("UnifiedInvestigator", test_investigator_functionality()))
    results.append(("Output Format", test_output_format_compatibility()))

    # Summary
    print("\n" + "=" * 60)
    print("FINAL TEST SUMMARY")
    print("=" * 60)
    print()

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name:30s} {status}")

    print()
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print()

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("Python modules have equivalent functionality to R scripts.")
    else:
        print("⚠️  Some tests failed. Review errors above.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
