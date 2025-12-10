#!/bin/bash
# Example: Run ETL Pipeline in Docker
# Demonstrates how to run the ETL pipeline using Docker containers

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo "=== Running ETL Pipeline ==="
echo ""

# Option 1: Run in existing container
echo "Method 1: Using existing container"
docker-compose exec python-etl python scripts/etl/etl_pipeline.py

echo ""
echo "=== ETL Pipeline Complete ==="

# Option 2: Run in new container (commented out)
# echo "Method 2: Using new container"
# docker-compose run --rm python-etl python scripts/etl/etl_pipeline.py
