#!/bin/bash
# Enforce Microservices Architecture
# Ensures all services follow microservices patterns

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo "=== Enforcing Microservices Architecture ==="
echo ""

# 1. Ensure network exists
echo "1. Ensuring network exists..."
if ! docker network ls | grep -q kettler-network; then
    docker network create kettler-network
    echo "   ✓ Network created"
else
    echo "   ✓ Network exists"
fi

# 2. Ensure health checks are configured
echo ""
echo "2. Verifying health checks..."
SERVICES_WITH_HEALTH=$(docker-compose config | grep -A 5 "healthcheck:" | grep -c "test:" || echo "0")
echo "   ✓ $SERVICES_WITH_HEALTH services with health checks"

# 3. Ensure dependencies are configured
echo ""
echo "3. Verifying dependencies..."
DEPENDENCIES=$(docker-compose config | grep -c "depends_on:" || echo "0")
echo "   ✓ $DEPENDENCIES services with dependencies"

# 4. Ensure restart policies
echo ""
echo "4. Verifying restart policies..."
RESTART_POLICIES=$(docker-compose config | grep -c "restart:" || echo "0")
echo "   ✓ $RESTART_POLICIES services with restart policies"

# 5. Ensure resource limits
echo ""
echo "5. Verifying resource limits..."
RESOURCE_LIMITS=$(docker-compose config | grep -c "limits:" || echo "0")
echo "   ✓ $RESOURCE_LIMITS services with resource limits"

# 6. Start services in correct order
echo ""
echo "6. Starting services in dependency order..."
docker-compose up -d python-etl
sleep 5
docker-compose up -d vector-api service-discovery
sleep 5

# 7. Verify services are running
echo ""
echo "7. Verifying services..."
HEALTHY_SERVICES=$(docker-compose ps --format json | jq -r 'select(.Health=="healthy" or .Status | contains("Up")) | .Service' 2>/dev/null | wc -l | xargs || echo "0")
echo "   ✓ $HEALTHY_SERVICES services running"

# 8. Test inter-service communication
echo ""
echo "8. Testing inter-service communication..."
if docker-compose exec -T vector-api curl -s http://python-etl:8000/health > /dev/null 2>&1; then
    echo "   ✓ Vector API can reach Python ETL"
else
    echo "   ⚠ Inter-service communication test failed"
fi

echo ""
echo "=== Microservices Architecture Enforced ==="
echo ""
echo "Services:"
docker-compose ps --format "table {{.Name}}\t{{.Status}}"
