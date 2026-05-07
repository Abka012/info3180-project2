#!/bin/bash
set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# ✅ Export absolute project root for Node script
export PROJECT_ROOT
echo "🔧 Exported PROJECT_ROOT=$PROJECT_ROOT"  # Debug line

# PID file for dev server
DEV_SERVER_PID=""

# Cleanup function
cleanup() {
    if [ -n "$FLASK_PID" ] && kill -0 "$FLASK_PID" 2>/dev/null; then
        echo -e "${YELLOW}🧹 Cleaning up: Stopping Flask server (PID: $FLASK_PID)...${NC}"
        kill "$FLASK_PID" 2>/dev/null || true
        wait "$FLASK_PID" 2>/dev/null || true
    fi
    if [ -n "$DEV_SERVER_PID" ] && kill -0 "$DEV_SERVER_PID" 2>/dev/null; then
        echo -e "${YELLOW}🧹 Cleaning up: Stopping dev server (PID: $DEV_SERVER_PID)...${NC}"
        kill "$DEV_SERVER_PID" 2>/dev/null || true
        wait "$DEV_SERVER_PID" 2>/dev/null || true
    fi
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📸 Dating App Documentation Screenshot Pipeline${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Check dependencies
echo -e "${YELLOW}📦 Checking dependencies...${NC}"
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python not found. Please install Python.${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js.${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found. Please install npm.${NC}"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD=$(command -v python3 || command -v python)
echo -e "${GREEN}✓ Python found: $($PYTHON_CMD --version)${NC}"
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
echo ""

# Step 2: Seed database in screenshot mode
echo -e "${YELLOW}🌱 Step 1/4: Seeding database (screenshot mode)...${NC}"
$PYTHON_CMD app/seed.py --screenshot-mode
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database seeded successfully!${NC}"
else
    echo -e "${RED}❌ Failed to seed database${NC}"
    exit 1
fi
echo ""

# Step 3: Start Flask backend in background
echo -e "${YELLOW}🚀 Step 2/4: Starting Flask backend...${NC}"
FLASK_PID=""
if [ -f "run.py" ]; then
    python3 run.py > /tmp/dating-app-flask.log 2>&1 &
    FLASK_PID=$!
    echo "   Flask PID: $FLASK_PID"
fi

# Start dev server in background
echo -e "${YELLOW}🚀 Step 2/4: Starting development server...${NC}"
npm run dev > /tmp/dating-app-dev.log 2>&1 &
DEV_SERVER_PID=$!
echo "   Dev server PID: $DEV_SERVER_PID"

# Wait for servers to be ready (max 60 seconds)
echo -n "   Waiting for servers to start"
flask_ready=false
dev_ready=false

for i in {1..120}; do
    # Check Flask backend
    if [ -n "$FLASK_PID" ] && [ "$flask_ready" = "false" ]; then
        if curl -s --connect-timeout 1 "http://127.0.0.1:5000/" > /dev/null 2>&1; then
            echo -e "\n${GREEN}✅ Flask backend is ready!${NC}"
            flask_ready=true
        fi
    fi

    # Check Vite dev server
    if [ "$dev_ready" = "false" ]; then
        for addr in "127.0.0.1" "localhost"; do
            if curl -s --connect-timeout 1 "http://$addr:5173" > /dev/null 2>&1; then
                echo -e "${GREEN}✅ Dev server is ready!${NC}"
                dev_ready=true
                break
            fi
        done
    fi

    # Check if processes are still running
    if [ -n "$FLASK_PID" ] && ! kill -0 "$FLASK_PID" 2>/dev/null; then
        echo -e "\n${RED}❌ Flask process died${NC}"
        echo "   Last 20 lines of Flask log:"
        tail -20 /tmp/dating-app-flask.log
        exit 1
    fi

    if ! kill -0 "$DEV_SERVER_PID" 2>/dev/null; then
        echo -e "\n${RED}❌ Dev server process died${NC}"
        echo "   Last 20 lines of dev log:"
        tail -20 /tmp/dating-app-dev.log
        exit 1
    fi

    # Both ready?
    if [ "$flask_ready" = "true" ] && [ "$dev_ready" = "true" ]; then
        echo ""
        break
    fi

    echo -n "."
    sleep 0.5
done

if [ "$dev_ready" != "true" ]; then
    echo -e "\n${RED}❌ Dev server failed to start within 60 seconds${NC}"
    echo "   Check /tmp/dating-app-dev.log for details:"
    tail -20 /tmp/dating-app-dev.log
    exit 1
fi

if [ -n "$FLASK_PID" ] && [ "$flask_ready" != "true" ]; then
    echo -e "\n${RED}❌ Flask backend failed to start within 60 seconds${NC}"
    echo "   Check /tmp/dating-app-flask.log for details:"
    tail -20 /tmp/dating-app-flask.log
    exit 1
fi
echo ""

# Step 4: Take screenshots
echo -e "${YELLOW}📸 Step 3/4: Capturing screenshots (light + dark)...${NC}"
if [ "$1" == "--force" ]; then
    echo "   Using --force flag (overwrite existing images)"
    node take-screenshots.js --force
else
    node take-screenshots.js
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Screenshots captured successfully!${NC}"
else
    echo -e "${RED}❌ Screenshot capture failed${NC}"
    exit 1
fi
echo ""

# Step 5: Generate markdown tables
echo -e "${YELLOW}📝 Step 4/4: Generating markdown tables...${NC}"
$PYTHON_CMD docs/generate_image_tables.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Markdown tables updated!${NC}"
else
    echo -e "${RED}❌ Failed to generate markdown tables${NC}"
    exit 1
fi
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ All done! Documentation pipeline complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "📊 Summary:"
echo "   - Database seeded (screenshot mode)"
echo "   - Screenshots captured: $(ls -1 docs/images/*.png 2>/dev/null | wc -l) images"
echo "   - User manual updated: docs/user_manual.md"
echo ""
echo "🔍 Next steps:"
echo "   1. Review screenshots in docs/images/"
echo "   2. Check docs/user_manual.md for image tables"
echo "   3. Commit changes: git add docs/ && git commit -m 'docs: update screenshots'"
