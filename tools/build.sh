#!/bin/bash
set -e

FORCE=${1:-""}
export PATH="/c/flutter/flutter/bin:$PATH"

generate_if_needed() {
    local script=$1
    local output=$2
    if [ ! -f "$output" ] || [ "$FORCE" = "--force" ]; then
        echo "-> Generating $output..."
        py "$script"
    else
        echo "ok $output exists, skipping"
    fi
}

echo "=== Data generation ==="
# World
generate_if_needed "tools/world/generate_pacific_islands.py" "assets/pacific_islands.json"
generate_if_needed "tools/world/generate_departments.py"     "assets/french_departments.json"
generate_if_needed "tools/world/generate_countries.py"       "assets/countries.json"
# History
generate_if_needed "tools/history/generate_kings_of_france.py"       "assets/kings_of_france.json"
generate_if_needed "tools/history/generate_american_presidents.py"   "assets/american_presidents.json"
# Space
generate_if_needed "tools/space/generate_exoplanets.py" "assets/exoplanets.json"
generate_if_needed "tools/space/generate_stars.py"      "assets/stars.json"
generate_if_needed "tools/space/generate_moons.py"      "assets/solar_moons.json"
# Cinema
generate_if_needed "tools/cinema/generate_classic_cinema.py" "assets/quotes_classic.json"
generate_if_needed "tools/cinema/generate_80s90s_cinema.py"  "assets/quotes_80s90s.json"
generate_if_needed "tools/cinema/generate_modern_cinema.py"  "assets/quotes_modern.json"

echo ""
echo "=== Flutter build ==="
flutter build appbundle --dart-define-from-file=env.json

echo ""
echo "AAB: build/app/outputs/bundle/release/app-release.aab"
