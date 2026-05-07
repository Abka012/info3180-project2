.PHONY: docs-seed docs-screenshots docs-generate-tables docs-all docs-clean

# Seed database for screenshots
docs-seed:
	python app/seed.py --screenshot-mode

# Take all screenshots (requires dev server running on :5173)
docs-screenshots:
	node take-screenshots.js

# Take specific routes only
docs-screenshots-custom:
	@read -p "Enter routes (e.g., /home /chat): " routes; \
	node take-screenshots.js $$routes

# Force re-capture all screenshots (overwrite existing)
docs-screenshots-force:
	node take-screenshots.js --force

# Generate markdown tables for user_manual.md
docs-generate-tables:
	python docs/generate_image_tables.py

# Full pipeline: seed -> screenshot -> generate tables
docs-all: docs-seed
	@echo "Starting dev server in background..."
	@npm run dev & sleep 5
	make docs-screenshots
	make docs-generate-tables
	@echo "✅ Documentation pipeline complete!"

# Clean all generated images
docs-clean:
	rm -f docs/images/*.png
	@echo "🧹 Cleaned docs/images/"

# Verify screenshot setup
docs-verify:
	@echo "=== Verification ==="
	@ls -la docs/images/*.png 2>/dev/null | wc -l | xargs -I {} echo "Images found: {}"
	@grep -c "SCREENSHOT_TABLES_START" docs/user_manual.md 2>/dev/null || echo "Markers not found in user_manual.md"
