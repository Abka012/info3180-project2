#!/bin/bash

show_help() {
    echo "DriftDater Test Runner"
    echo "======================"
    echo ""
    echo "Usage: ./run-tests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all           Run all tests (default)"
    echo "  --api           Run API tests only"
    echo "  --matching      Run matching tests only"
    echo "  --messaging     Run messaging tests only"
    echo "  --search        Run search tests only"
    echo "  --coverage      Run all tests with coverage report"
    echo "  --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run-tests.sh              # Run all tests"
    echo "  ./run-tests.sh --api        # Run API tests only"
    echo "  ./run-tests.sh --coverage   # Run all tests with coverage"
}

run_all() {
    source .venv/bin/activate
    echo "Running all tests..."
    pytest tests/ -v --tb=short
}

run_api() {
    source .venv/bin/activate
    echo "Running API tests..."
    pytest tests/test_api.py -v --tb=short
}

run_matching() {
    source .venv/bin/activate
    echo "Running matching tests..."
    pytest tests/test_matching.py -v --tb=short
}

run_messaging() {
    source .venv/bin/activate
    echo "Running messaging tests..."
    pytest tests/test_messaging.py -v --tb=short
}

run_search() {
    source .venv/bin/activate
    echo "Running search tests..."
    pytest tests/test_search.py -v --tb=short
}

run_coverage() {
    source .venv/bin/activate
    echo "Running all tests with coverage..."
    pytest tests/ -v --tb=short --cov=. --cov-report=html --cov-report=term-missing
    echo ""
    echo "Coverage report generated at: htmlcov/index.html"
}

if [ $# -eq 0 ]; then
    run_all
else
    case "$1" in
        --all)
            run_all
            ;;
        --api)
            run_api
            ;;
        --matching)
            run_matching
            ;;
        --messaging)
            run_messaging
            ;;
        --search)
            run_search
            ;;
        --coverage)
            run_coverage
            ;;
        --help|-h)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
fi

echo ""
echo "==========================="
echo "Tests complete!"
