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
generate_if_needed "tools/world/generate_pacific_islands.py" "assets/world/pacific_islands.json"
generate_if_needed "tools/world/generate_departments.py"     "assets/world/french_departments.json"
generate_if_needed "tools/world/generate_countries.py"       "assets/world/countries.json"
generate_if_needed "tools/world/generate_communes.py"        "assets/world/communes.json"
generate_if_needed "tools/world/generate_american_states.py" "assets/world/american_states.json"
generate_if_needed "tools/world/generate_deserts.py"         "assets/world/deserts.json"
generate_if_needed "tools/world/generate_rivers.py"          "assets/world/rivers.json"
generate_if_needed "tools/world/generate_seas.py"            "assets/world/seas.json"
# History
generate_if_needed "tools/history/generate_kings_of_france.py"       "assets/history/kings_of_france.json"
generate_if_needed "tools/history/generate_american_presidents.py"   "assets/history/american_presidents.json"
# Space
generate_if_needed "tools/space/generate_exoplanets.py" "assets/space/exoplanets.json"
generate_if_needed "tools/space/generate_stars.py"      "assets/space/stars.json"
generate_if_needed "tools/space/generate_moons.py"      "assets/space/solar_moons.json"
# History battles
generate_if_needed "tools/history/generate_battles.py" "assets/history/battles.json"
# Science
generate_if_needed "tools/science/generate_dinosaurs.py"         "assets/science/dinosaurs.json"
generate_if_needed "tools/science/generate_chemical_elements.py" "assets/science/chemical_elements.json"
generate_if_needed "tools/science/generate_volcanoes.py"         "assets/science/volcanoes.json"
generate_if_needed "tools/science/generate_insects.py"           "assets/science/insects.json"
generate_if_needed "tools/science/generate_birds.py"             "assets/science/birds.json"
generate_if_needed "tools/science/generate_minerals.py"          "assets/science/minerals.json"
generate_if_needed "tools/science/generate_clouds.py"            "assets/science/clouds.json"
generate_if_needed "tools/science/generate_human_bones.py"       "assets/science/human_bones.json"
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
# Celebrity
generate_if_needed "tools/celebrity/generate_lgbtqia.py"             "assets/celebrity/lgbtqia.json"
generate_if_needed "tools/celebrity/generate_pioneer_women.py"       "assets/celebrity/pioneer_women.json"
generate_if_needed "tools/celebrity/generate_legendary_athletes.py"  "assets/celebrity/legendary_athletes.json"
# Cinema
generate_if_needed "tools/cinema/generate_classic_cinema.py" "assets/cinema/quotes_classic.json"
generate_if_needed "tools/cinema/generate_80s90s_cinema.py"  "assets/cinema/quotes_80s90s.json"
generate_if_needed "tools/cinema/generate_modern_cinema.py"  "assets/cinema/quotes_modern.json"

echo ""
echo "=== Flutter build ==="
flutter build appbundle --release --dart-define-from-file=env.json

echo ""
echo "AAB: build/app/outputs/bundle/release/app-release.aab"
