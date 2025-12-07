#!/bin/bash
# Example: Parallel Execution
# Demonstrates running multiple tasks in parallel using Docker

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo "=== Parallel Execution Example ==="
echo ""

# Scale services for parallel execution
echo "1. Scaling Python ETL to 5 instances:"
docker-compose up -d --scale python-etl=5

echo ""
echo "2. Waiting for services to start..."
sleep 5

echo ""
echo "3. Current service status:"
docker-compose ps | grep python-etl

echo ""
echo "4. Running parallel ETL tasks:"
# Run ETL in multiple containers simultaneously
for i in {1..3}; do
    echo "  Starting task $i..."
    docker-compose exec -d python-etl python scripts/etl/etl_pipeline.py --dir data/source
done

echo ""
echo "5. Monitoring task execution:"
sleep 3
docker-compose ps | grep python-etl

echo ""
echo "=== Parallel Execution Complete ==="
echo ""
echo "To view logs:"
echo "  docker-compose logs -f python-etl"
echo ""
echo "To scale down:"
echo "  docker-compose up -d --scale python-etl=1"
