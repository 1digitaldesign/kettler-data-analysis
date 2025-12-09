#!/bin/bash
# Run all tests to verify Python modules match R script functionality

set -e

echo "============================================================"
echo "Running All Tests: Python Modules vs R Scripts"
echo "============================================================"
echo ""

cd "$(dirname "$0")/.."

# Set Python path
export PYTHONPATH=.

# Run functionality comparison test
echo "Test 1: Functionality Comparison"
echo "--------------------------------"
python3 tests/test_functionality_comparison.py
echo ""

# Run output comparison test
echo "Test 2: Output Comparison"
echo "-------------------------"
python3 tests/compare_r_python_outputs.py
echo ""

echo "============================================================"
echo "All Tests Complete"
echo "============================================================"
