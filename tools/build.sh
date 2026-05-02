#!/bin/bash
set -e

FORCE=${1:-""}
export PATH="/c/flutter/flutter/bin:$PATH"

generate_if_needed() {
    local script=$1
    local output=$2
    if [ ! -f "$output" ] || [ "$FORCE" = "--force" ]; then
        echo "→ Generating $output..."
        py "$script"
    else
        echo "✓ $output exists, skipping"
    fi
}

echo "=== Data generation ==="
generate_if_needed "tools/generate_pacific_islands.py" "assets/pacific_islands.json"
generate_if_needed "tools/generate_departments.py"     "assets/french_departments.json"
generate_if_needed "tools/generate_countries.py"       "assets/countries.json"

echo ""
echo "=== Flutter build ==="
flutter build appbundle --dart-define-from-file=env.json

echo ""
echo "✅ AAB: build/app/outputs/bundle/release/app-release.aab"
