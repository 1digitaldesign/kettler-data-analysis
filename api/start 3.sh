#!/bin/bash
# Start the FastAPI server

echo "Starting Kettler Data Analysis API Server..."
echo ""

cd "$(dirname "$0")/.."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies if needed
python3 -c "import fastapi" 2>/dev/null || {
    echo "Installing API dependencies..."
    pip install fastapi uvicorn pydantic
}

echo "Starting API server on http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
echo ""

python3 api/server.py
