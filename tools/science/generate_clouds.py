#!/usr/bin/env python3
"""Generate assets/science/clouds.json — fetch images from Wikipedia/Wikimedia."""

import json, time, urllib.parse, urllib.request, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from clouds_raw import CLOUDS

OUTPUT = os.path.join(os.path.dirname(__file__), '../../assets/science/clouds.json')

WIKI_TITLE_OVERRIDES = {
    "Cirrus":                        "Cirrus cloud",
    "Cirrocumulus":                  "Cirrocumulus cloud",
    "Cirrostratus":                  "Cirrostratus cloud",
    "Altocumulus":                   "Altocumulus cloud",
    "Altostratus":                   "Altostratus cloud",
    "Nimbostratus":                  "Nimbostratus cloud",
    "Stratocumulus":                 "Stratocumulus cloud",
    "Stratus":                       "Stratus cloud",
    "Cumulus":                       "Cumulus cloud",
    "Cumulonimbus":                  "Cumulonimbus cloud",
    "Cirrus fibratus":               "Cirrus fibratus",
    "Cirrus uncinus":                "Cirrus uncinus",
    "Cirrus spissatus":              "Cirrus spissatus",
    "Altocumulus lenticularis":      "Lenticular cloud",
    "Altocumulus castellanus":       "Altocumulus castellanus",
    "Altocumulus floccus":           "Altocumulus floccus",
    "Stratocumulus lenticularis":    "Lenticular cloud",
    "Cumulus humilis":               "Cumulus humilis",
    "Cumulus congestus":             "Cumulus congestus",
    "Cumulonimbus capillatus":       "Cumulonimbus cloud",
    "Cumulonimbus calvus":           "Cumulonimbus cloud",
    "Mammatus":                      "Mammatus cloud",
    "Arcus (Shelf cloud)":           "Shelf cloud",
    "Virga":                         "Virga",
    "Pileus":                        "Pileus (meteorology)",
    "Asperitas":                     "Asperitas cloud",
    "Fluctus":                       "Kelvin-Helmholtz instability",
    "Cavum (Fallstreak hole)":       "Fallstreak hole",
    "Murus (Wall cloud)":            "Wall cloud",
    "Tuba (Funnel cloud)":           "Funnel cloud",
    "Incus (Anvil cloud)":           "Cumulonimbus incus",
    "Velum":                         "Velum (cloud)",
    "Pannus":                        "Pannus (cloud)",
    "Noctilucent cloud (NLC)":       "Noctilucent cloud",
    "Nacreous cloud":                "Nacreous cloud",
    "Pyrocumulonimbus":              "Pyrocumulonimbus",
    "Morning Glory":                 "Morning glory cloud",
    "Orographic cap cloud":          "Cap cloud",
    "Contrail":                      "Contrail",
    "Ship track":                    "Ship tracks",
    "Fog":                           "Fog",
    "Altocumulus undulatus":         "Altocumulus cloud",
    "Cirrocumulus undulatus":        "Cirrocumulus undulatus",
    "Cloud streets (Cumulus radiatus)": "Cloud street",
    "Stratocumulus opacus":          "Stratocumulus cloud",
}

SKIP_EXTENSIONS = {".svg", ".gif"}

def fetch_wiki_image(title: str) -> str | None:
    title_enc = urllib.parse.quote(title.replace(" ", "_"))
    url = (
        f"https://en.wikipedia.org/w/api.php?action=query&titles={title_enc}"
        "&prop=pageimages&format=json&pithumbsize=600"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.load(r)
        pages = data["query"]["pages"]
        page = next(iter(pages.values()))
        thumb = page.get("thumbnail", {}).get("source")
        if not thumb:
            return None
        ext = os.path.splitext(thumb.split("?")[0])[1].lower()
        if ext in SKIP_EXTENSIONS:
            return None
        return thumb
    except Exception as e:
        print(f"  WARNING: {title} — {e}")
        return None

def main():
    existing: list = []
    if os.path.exists(OUTPUT):
        with open(OUTPUT, encoding="utf-8") as f:
            existing = json.load(f)
    existing_map = {e["n"]: e for e in existing}

    result = []
    for cloud in CLOUDS:
        name = cloud["n"]
        if name in existing_map and existing_map[name].get("im") is not None:
            print(f"  skip (cached)  {name}")
            result.append({**cloud, "im": existing_map[name]["im"]})
            continue

        wiki_title = WIKI_TITLE_OVERRIDES.get(name, name)
        print(f"  fetch  {name}  →  {wiki_title}")
        image_url = fetch_wiki_image(wiki_title)
        result.append({**cloud, "im": image_url})
        time.sleep(0.3)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {len(result)} clouds → {OUTPUT}")

if __name__ == "__main__":
    main()
