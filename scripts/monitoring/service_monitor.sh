#!/bin/bash
# Service Monitor Script
# Monitors Docker services and provides status updates

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo "=== Docker Service Monitor ==="
echo "Timestamp: $(date)"
echo ""

# Check Docker Compose services
echo "--- Service Status ---"
docker-compose ps

echo ""
echo "--- Resource Usage ---"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | head -10

echo ""
echo "--- Health Checks ---"

# Vector API
if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Vector API: Healthy"
else
    echo "❌ Vector API: Unhealthy"
fi

# R API
if curl -s -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ R API: Healthy"
else
    echo "❌ R API: Unhealthy or not running"
fi

echo ""
echo "--- Recent Logs (last 5 lines) ---"
echo "Vector API:"
docker-compose logs --tail=5 vector-api 2>/dev/null || echo "No logs available"
echo ""
echo "Python ETL:"
docker-compose logs --tail=5 python-etl 2>/dev/null | head -5 || echo "No logs available"
