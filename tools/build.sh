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
generate_if_needed "tools/world/generate_communes.py"        "assets/world/communes.json"
generate_if_needed "tools/world/generate_american_states.py" "assets/world/american_states.json"
# History
generate_if_needed "tools/history/generate_kings_of_france.py"       "assets/kings_of_france.json"
generate_if_needed "tools/history/generate_american_presidents.py"   "assets/american_presidents.json"
# Space
generate_if_needed "tools/space/generate_exoplanets.py" "assets/exoplanets.json"
generate_if_needed "tools/space/generate_stars.py"      "assets/stars.json"
generate_if_needed "tools/space/generate_moons.py"      "assets/solar_moons.json"
# History battles
generate_if_needed "tools/history/generate_battles.py" "assets/history/battles.json"
# Science
generate_if_needed "tools/science/generate_dinosaurs.py"         "assets/science/dinosaurs.json"
generate_if_needed "tools/science/generate_chemical_elements.py" "assets/science/chemical_elements.json"
generate_if_needed "tools/science/generate_volcanoes.py"         "assets/science/volcanoes.json"
# Space missions
generate_if_needed "tools/space/generate_space_missions.py" "assets/space/missions.json"
# Art
generate_if_needed "tools/art/generate_paintings.py"           "assets/art/paintings.json"
generate_if_needed "tools/art/generate_sculptures.py"          "assets/art/sculptures.json"
generate_if_needed "tools/art/generate_architecture.py"        "assets/art/architecture.json"
generate_if_needed "tools/art/generate_famous_artists.py"      "assets/art/famous_artists.json"
generate_if_needed "tools/art/generate_photographers.py"       "assets/art/photographers.json"
generate_if_needed "tools/art/generate_classical_composers.py" "assets/art/classical_composers.json"
generate_if_needed "tools/art/generate_nobel_prize.py"         "assets/art/nobel_prize.json"
# Cinema
generate_if_needed "tools/cinema/generate_classic_cinema.py" "assets/quotes_classic.json"
generate_if_needed "tools/cinema/generate_80s90s_cinema.py"  "assets/quotes_80s90s.json"
generate_if_needed "tools/cinema/generate_modern_cinema.py"  "assets/quotes_modern.json"

echo ""
echo "=== Flutter build ==="
flutter build appbundle --release --dart-define-from-file=env.json

echo ""
echo "AAB: build/app/outputs/bundle/release/app-release.aab"
