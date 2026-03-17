#!/bin/bash

echo "=== Starting DriftDater ==="

# Kill any existing processes
echo "Cleaning up ports..."
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
sleep 1

# Start Backend
echo "Starting Backend (Flask)..."
source .venv/bin/activate
python run.py > /tmp/flask.log 2>&1 &
BACKEND_PID=$!

sleep 3

# Start Frontend
echo "Starting Frontend (Vite)..."
npm run dev -- --host 0.0.0.0 > /tmp/vite.log 2>&1 &
FRONTEND_PID=$!

echo ""
echo "=== DriftDater is running ==="
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo ""
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
echo "Press Ctrl+C to stop all..."

# Wait for any signal
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
