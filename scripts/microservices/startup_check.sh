#!/bin/bash
# Startup Check Script
# Ensures all microservices dependencies are available before starting

set -e

SERVICE_NAME=${SERVICE_NAME:-unknown}
MAX_WAIT=${MAX_WAIT:-60}
WAIT_INTERVAL=${WAIT_INTERVAL:-2}

echo "=== Startup Check for $SERVICE_NAME ==="
echo "Waiting for dependencies..."

# Wait for service discovery if needed
if [ -n "$SERVICE_DISCOVERY_URL" ]; then
    echo "Waiting for service discovery..."
    wait_count=0
    while [ $wait_count -lt $MAX_WAIT ]; do
        if curl -s -f "$SERVICE_DISCOVERY_URL/health" > /dev/null 2>&1; then
            echo "✓ Service discovery available"
            break
        fi
        wait_count=$((wait_count + WAIT_INTERVAL))
        sleep $WAIT_INTERVAL
    done

    if [ $wait_count -ge $MAX_WAIT ]; then
        echo "⚠ Service discovery not available, continuing anyway"
    fi
fi

# Wait for data directory
if [ -n "$DATA_DIR" ]; then
    if [ ! -d "$DATA_DIR" ]; then
        echo "Creating data directory: $DATA_DIR"
        mkdir -p "$DATA_DIR"
    fi
    echo "✓ Data directory available"
fi

echo "=== Startup Check Complete ==="
echo "Starting service: $SERVICE_NAME"
