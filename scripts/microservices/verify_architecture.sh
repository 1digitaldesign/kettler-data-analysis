#!/bin/bash
# Verify Microservices Architecture
# Ensures all services are properly configured and communicating

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo "=== Verifying Microservices Architecture ==="
echo ""

# Check Docker Compose services
echo "1. Checking Docker Compose services..."
SERVICES=$(docker-compose ps --services)
SERVICE_COUNT=$(echo "$SERVICES" | wc -l | xargs)
echo "   Found $SERVICE_COUNT services"

# Check network
echo ""
echo "2. Checking network..."
if docker network ls | grep -q kettler-network; then
    echo "   ✓ Network 'kettler-network' exists"
    NETWORK_ID=$(docker network ls | grep kettler-network | awk '{print $1}')
    CONTAINERS=$(docker network inspect $NETWORK_ID --format '{{range .Containers}}{{.Name}} {{end}}')
    CONTAINER_COUNT=$(echo $CONTAINERS | wc -w | xargs)
    echo "   ✓ $CONTAINER_COUNT containers connected"
else
    echo "   ✗ Network 'kettler-network' not found"
fi

# Check health checks
echo ""
echo "3. Checking service health..."
for service in $SERVICES; do
    HEALTH=$(docker-compose ps --format json | jq -r "select(.Service==\"$service\") | .Health" 2>/dev/null || echo "unknown")
    STATUS=$(docker-compose ps --format json | jq -r "select(.Service==\"$service\") | .Status" 2>/dev/null || echo "unknown")

    if [ "$HEALTH" = "healthy" ] || [ "$STATUS" = "Up" ]; then
        echo "   ✓ $service: $STATUS ($HEALTH)"
    else
        echo "   ⚠ $service: $STATUS ($HEALTH)"
    fi
done

# Check service discovery
echo ""
echo "4. Checking service discovery..."
if docker-compose ps | grep -q service-discovery; then
    sleep 2
    if curl -s -f http://localhost:8080/health > /dev/null 2>&1; then
        echo "   ✓ Service discovery responding"
        SERVICES_LIST=$(curl -s http://localhost:8080/api/v1/services 2>/dev/null | jq -r '.services | keys[]' 2>/dev/null || echo "")
        if [ -n "$SERVICES_LIST" ]; then
            echo "   ✓ Registered services: $(echo $SERVICES_LIST | tr '\n' ' ')"
        fi
    else
        echo "   ⚠ Service discovery not responding"
    fi
else
    echo "   ⚠ Service discovery not running"
fi

# Check inter-service communication
echo ""
echo "5. Testing inter-service communication..."
if docker-compose exec -T vector-api python -c "from scripts.microservices.service_client import get_service_client; client = get_service_client(); print('✓ Service client initialized')" 2>/dev/null; then
    echo "   ✓ Service client working"
else
    echo "   ⚠ Service client not available"
fi

echo ""
echo "=== Verification Complete ==="
