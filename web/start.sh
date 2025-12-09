#!/bin/bash
# Start the web development server

echo "Starting Kettler Data Analysis Web Application..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo "Starting Vite dev server..."
echo "Open http://localhost:3000 in your browser"
echo ""

npm run dev
