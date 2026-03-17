#!/bin/bash

echo "Running DriftDater Tests..."
echo "==========================="

source .venv/bin/activate

pytest tests/ -v --tb=short

echo ""
echo "==========================="
echo "Tests complete!"
