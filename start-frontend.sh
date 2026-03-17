#!/bin/bash

# Kill any process on port 5173
echo "Killing any process on port 5173..."
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

# Wait a moment
sleep 1

# Start Vite dev server
echo "Starting Frontend..."
npm run dev -- --host 0.0.0.0
