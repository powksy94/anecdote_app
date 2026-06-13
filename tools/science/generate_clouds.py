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
    "Arcus (Shelf cloud)":           "Arcus cloud",
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
    "Nacreous cloud":                "Polar stratospheric cloud",
    "Pyrocumulonimbus":              "Pyrocumulonimbus",
    "Morning Glory":                 "Morning Glory cloud",
    "Orographic cap cloud":          "Orographic lift",
    "Contrail":                      "Contrail",
    "Ship track":                    "Ship tracks",
    "Fog":                           "Fog",
    "Altocumulus undulatus":         "Altocumulus cloud",
    "Cirrocumulus undulatus":        "Cirrocumulus undulatus",
    "Cloud streets (Cumulus radiatus)": "Cloud street",
    "Stratocumulus opacus":          "Stratocumulus cloud",
}

# Direct URL overrides — Wikipedia/Commons both return a lichen for "Asperitas"
IMAGE_OVERRIDES = {
    "Asperitas": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Undulatus_asperitas_Bustubaevo_village_Bashkortostan_Russia.jpg/960px-Undulatus_asperitas_Bustubaevo_village_Bashkortostan_Russia.jpg",
}

SKIP_EXTENSIONS = {".svg", ".gif"}

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

def fetch_wiki_image(title: str) -> str | None:
    title_enc = urllib.parse.quote(title.replace(" ", "_"))
    url = (
        f"https://en.wikipedia.org/w/api.php?action=query&titles={title_enc}"
        "&prop=pageimages&format=json&pithumbsize=600"
    )
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
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
        sys.stdout.buffer.write(f"  WARNING: {title} -- {e}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        return None

def fetch_commons_image(query: str) -> str | None:
    enc = urllib.parse.quote(query)
    url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrsearch={enc}&gsrnamespace=6&gsrlimit=5"
        "&prop=imageinfo&iiprop=url&iiurlwidth=600&format=json"
    )
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
        pages = data.get("query", {}).get("pages", {})
        for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
            infos = page.get("imageinfo", [])
            if infos:
                img_url = infos[0].get("thumburl") or infos[0].get("url")
                if img_url:
                    ext = os.path.splitext(img_url.split("?")[0])[1].lower()
                    if ext not in SKIP_EXTENSIONS:
                        return img_url
    except Exception:
        pass
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
            sys.stdout.buffer.write(f"  skip (cached)  {name}\n".encode("utf-8")); sys.stdout.buffer.flush()
            result.append({**cloud, "im": existing_map[name]["im"]})
            continue

        if name in IMAGE_OVERRIDES:
            sys.stdout.buffer.write(f"  override  {name}\n".encode("utf-8")); sys.stdout.buffer.flush()
            result.append({**cloud, "im": IMAGE_OVERRIDES[name]})
            continue

        wiki_title = WIKI_TITLE_OVERRIDES.get(name, name)
        sys.stdout.buffer.write(f"  fetch  {name}  ->  {wiki_title}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        image_url = fetch_wiki_image(wiki_title)
        if image_url is None:
            image_url = fetch_commons_image(f"{name} cloud")
        if image_url is None:
            image_url = fetch_commons_image(name)
        result.append({**cloud, "im": image_url})
        time.sleep(0.3)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    sys.stdout.buffer.write(f"\nWrote {len(result)} clouds -> {OUTPUT}\n".encode("utf-8"))

if __name__ == "__main__":
    main()
