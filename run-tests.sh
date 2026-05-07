#!/bin/bash

show_help() {
    echo "DriftDater Test Runner"
    echo "======================"
    echo ""
    echo "Usage: ./run-tests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all           Run all tests (default)"
    echo "  --auth          Run authentication tests only"
    echo "  --matches       Run match algorithm tests only"
    echo "  --notifications Run notification tests only"
    echo "  --messaging     Run messaging tests only"
    echo "  --profile       Run profile tests only"
    echo "  --search        Run search tests only"
    echo "  --fast          Run core tests only (auth, seed, utils, migrations)"
    echo "  --coverage      Run all tests with coverage report"
    echo "  --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run-tests.sh              # Run all tests"
    echo "  ./run-tests.sh --auth       # Run auth tests only"
    echo "  ./run-tests.sh --coverage   # Run all tests with coverage"
}

run_all() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Cleaning up generated test images..."
    rm -rf uploads/profile_pics/*.png
    rm -rf uploads/profile_pics/*.jpg
    rm -rf uploads/profile_pics/*.webp
    echo "Running all tests..."
    pytest tests/ -v --tb=short
}

run_auth() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Running authentication tests..."
    pytest tests/test_auth.py -v --tb=short
}

run_matches() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Running match algorithm tests..."
    pytest tests/test_matches.py -v --tb=short
}

run_profile() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Running match algorithm tests..."
    pytest tests/test_profile.py -v --tb=short
}

run_notifications() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Running notification tests..."
    pytest tests/test_notifications.py -v --tb=short
}

run_messaging() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Running messaging tests..."
    pytest tests/test_messaging.py -v --tb=short
}

run_search() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Running search tests..."
    pytest tests/test_search.py -v --tb=short
}

run_fast() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Running core/fast tests..."
    pytest tests/test_auth.py tests/test_seed.py tests/test_utils.py tests/test_migrations.py -v --tb=short
}

run_coverage() {
    source .venv/bin/activate 2>/dev/null || true
    echo "Running all tests with coverage..."
    pytest tests/ -v --tb=short --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=30
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
        --auth)
            run_auth
            ;;
        --profile)
            run_profile
            ;;
        --matches)
            run_matches
            ;;
        --notifications)
            run_notifications
            ;;
        --messaging)
            run_messaging
            ;;
        --search)
            run_search
            ;;
        --fast)
            run_fast
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
