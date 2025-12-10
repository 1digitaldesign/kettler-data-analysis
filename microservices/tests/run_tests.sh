#!/bin/bash
# Comprehensive test runner for microservices

set -e

echo "=========================================="
echo "Microservices Test Suite"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test types
UNIT_TESTS="tests/test_analysis_service.py tests/test_api_gateway.py"
INTEGRATION_TESTS="tests/test_integration.py"
LOAD_TESTS="tests/test_load.py"
ALL_SERVICES_TESTS="tests/test_all_services.py"

# Function to run tests
run_tests() {
    local test_type=$1
    local test_files=$2
    local marker=$3

    echo ""
    echo -e "${YELLOW}Running $test_type tests...${NC}"

    if [ -n "$marker" ]; then
        pytest $test_files -m "$marker" -v
    else
        pytest $test_files -v
    fi

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $test_type tests passed${NC}"
        return 0
    else
        echo -e "${RED}✗ $test_type tests failed${NC}"
        return 1
    fi
}

# Check if services are running
check_services() {
    echo "Checking if services are running..."

    services=("8000:API Gateway" "8001:Analysis" "8002:Scraping" "8003:Validation" \
              "8004:Vector" "8005:GIS" "8006:ACRIS" "8007:Data" "8008:Google Drive")

    all_running=true
    for service in "${services[@]}"; do
        IFS=':' read -r port name <<< "$service"
        if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $name (port $port) is running${NC}"
        else
            echo -e "${YELLOW}⚠ $name (port $port) is not running${NC}"
            all_running=false
        fi
    done

    if [ "$all_running" = false ]; then
        echo ""
        echo -e "${YELLOW}Warning: Some services are not running. Some tests may fail.${NC}"
        echo "Start services with: docker-compose up"
    fi
}

# Main execution
main() {
    # Parse arguments
    TEST_TYPE=${1:-all}

    case $TEST_TYPE in
        unit)
            run_tests "Unit" "$UNIT_TESTS" "unit"
            ;;
        integration)
            check_services
            run_tests "Integration" "$INTEGRATION_TESTS" "integration"
            ;;
        load)
            check_services
            run_tests "Load" "$LOAD_TESTS" "load"
            ;;
        all-services)
            check_services
            run_tests "All Services" "$ALL_SERVICES_TESTS" ""
            ;;
        all)
            check_services
            run_tests "Unit" "$UNIT_TESTS" "unit"
            run_tests "Integration" "$INTEGRATION_TESTS" "integration"
            run_tests "All Services" "$ALL_SERVICES_TESTS" ""
            echo ""
            echo -e "${YELLOW}Skipping load tests (use 'load' to run them)${NC}"
            ;;
        coverage)
            echo "Running tests with coverage..."
            pytest --cov=../microservices --cov-report=html --cov-report=term-missing
            echo "Coverage report generated in htmlcov/"
            ;;
        *)
            echo "Usage: $0 [unit|integration|load|all-services|all|coverage]"
            exit 1
            ;;
    esac

    echo ""
    echo -e "${GREEN}=========================================="
    echo "Test Suite Complete"
    echo "==========================================${NC}"
}

main "$@"
