import json
from pathlib import Path

# Names whose "recovered" image came from the unreliable opensearch fallback
# and points to a clearly unrelated Wikipedia topic (verified by inspecting
# the resolved titles: e.g. "Garmin" for Garm, "Nottingham Forest F.C." for
# Nott, "Voronoi diagram" for Vor...). Reverting these back to no-image
# rather than shipping a wrong picture.
REVERT = {
    "assets/mythology/greek_mythology.json": {"Europa"},
    "assets/mythology/norse_mythology.json": {
        "Yggdrasil", "Asgard", "Midgard", "Dwarves (Norse)", "Elves (Norse)",
        "Buri", "Nott", "Kvasir", "Gerd", "Nanna", "Sindri", "Var", "Vor",
        "Syn", "Lofn", "Sjofn",
    },
    "assets/mythology/egyptian_mythology.json": {
        "Amun", "Geb", "Atum", "Wepwawet", "Hapi", "Meretseger",
        "Hapy (Son of Horus)",
    },
    "assets/mythology/mythological_creatures.json": {
        "Sphinx (Greek)", "Garm", "Wendigo",
    },
}

for path_str, names in REVERT.items():
    path = Path(path_str)
    data = json.loads(path.read_text(encoding="utf-8"))
    reverted = 0
    for entry in data:
        if entry["n"] in names:
            entry["im"] = None
            reverted += 1
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("{}: reverted {}".format(path_str, reverted))
