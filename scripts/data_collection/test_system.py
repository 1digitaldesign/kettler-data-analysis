#!/usr/bin/env python3
"""
System Test
Tests all progress bar and search components.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_progress_bars():
    """Test progress bar components."""
    print("Testing Progress Bar Components...")
    print("-" * 80)

    try:
        from progress_bar_module import ProgressBar
        pb = ProgressBar()
        overall = pb.get_overall_progress()
        print(f"✅ ProgressBar module: {overall:.1f}%")
    except Exception as e:
        print(f"❌ ProgressBar module: {e}")
        return False

    try:
        from progress_widget import ProgressWidget
        widget = ProgressWidget()
        sparkline = widget.sparkline()
        print(f"✅ ProgressWidget: {sparkline}")
    except Exception as e:
        print(f"❌ ProgressWidget: {e}")
        return False

    try:
        from progress_integration import get_progress_string
        progress_str = get_progress_string('compact')
        print(f"✅ Progress Integration: Working")
    except Exception as e:
        print(f"❌ Progress Integration: {e}")
        return False

    try:
        from progress_realtime import RealTimeProgress
        rt = RealTimeProgress()
        print(f"✅ RealTime Progress: Working")
    except Exception as e:
        print(f"❌ RealTime Progress: {e}")
        return False

    print()
    return True

def test_search_integration():
    """Test search integration."""
    print("Testing Search Integration...")
    print("-" * 80)

    try:
        from search_with_progress import SearchWithProgress
        swp = SearchWithProgress()
        status = swp.check_license_searches_status()
        print(f"✅ Search Integration: {status['complete']}/{status['total']} states")
    except Exception as e:
        print(f"❌ Search Integration: {e}")
        return False

    try:
        from search_dashboard import display_search_dashboard
        print(f"✅ Search Dashboard: Available")
    except Exception as e:
        print(f"❌ Search Dashboard: {e}")
        return False

    try:
        from search_workflow import SearchWorkflow
        workflow = SearchWorkflow()
        print(f"✅ Search Workflow: Available")
    except Exception as e:
        print(f"❌ Search Workflow: {e}")
        return False

    print()
    return True

def test_exports():
    """Test export functionality."""
    print("Testing Export Functionality...")
    print("-" * 80)

    try:
        from progress_bar_module import ProgressBar
        pb = ProgressBar()
        json_path = pb.export_json()
        csv_path = pb.export_csv()
        print(f"✅ JSON Export: {json_path.exists()}")
        print(f"✅ CSV Export: {csv_path.exists()}")
    except Exception as e:
        print(f"❌ Export: {e}")
        return False

    print()
    return True

def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print(" " * 25 + "🧪 SYSTEM TEST" + " " * 25)
    print("=" * 80)
    print()

    results = []

    # Test progress bars
    results.append(("Progress Bars", test_progress_bars()))

    # Test search integration
    results.append(("Search Integration", test_search_integration()))

    # Test exports
    results.append(("Exports", test_exports()))

    # Summary
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    print()

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("🎉 All tests passed! System is operational.")
    else:
        print("⚠️  Some tests failed. Please check errors above.")

    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
