#!/usr/bin/env python3
"""Generate assets/science/minerals.json — fetch images from Wikipedia/Wikimedia."""

import json, time, urllib.parse, urllib.request, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from minerals_raw import MINERALS

OUTPUT = os.path.join(os.path.dirname(__file__), '../../assets/science/minerals.json')

WIKI_TITLE_OVERRIDES = {
    "Amethyst":              "Amethyst",
    "Rose Quartz":           "Rose quartz",
    "Obsidian":              "Obsidian",
    "Feldspar (Orthoclase)": "Orthoclase",
    "Jade (Jadeite)":        "Jadeite",
    "Emerald":               "Emerald",
    "Aquamarine":            "Aquamarine",
    "Ruby":                  "Ruby",
    "Sapphire":              "Sapphire",
    "Bornite":               "Bornite",
    "Garnet (Almandine)":    "Almandine",
    "Opal":                  "Opal",
    "Peridot (Olivine)":     "Peridot",
    "Alexandrite":           "Alexandrite",
    "Spessartine Garnet":    "Spessartite",
    "Sugilite":              "Sugilite",
    "Tanzanite":             "Tanzanite",
    "Iolite":                "Iolite",
    "Vesuvianite":           "Vesuvianite",
    "Rhodonite":             "Rhodonite",
    "Chrysocolla":           "Chrysocolla",
    "Wulfenite":             "Wulfenite",
    "Realgar":               "Realgar",
    "Stibnite":              "Stibnite",
    "Smithsonite":           "Smithsonite",
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
        if thumb:
            ext = os.path.splitext(thumb.split("?")[0])[1].lower()
            if ext in SKIP_EXTENSIONS:
                return None
        return thumb
    except Exception:
        return None

def fetch_commons_image(title: str) -> str | None:
    query = urllib.parse.quote(title)
    url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrsearch={query}&gsrnamespace=6&gsrlimit=5"
        "&prop=imageinfo&iiprop=url&format=json"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.load(r)
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            infos = page.get("imageinfo", [])
            if infos:
                img_url = infos[0]["url"]
                ext = os.path.splitext(img_url.split("?")[0])[1].lower()
                if ext not in SKIP_EXTENSIONS:
                    return img_url
    except Exception:
        pass
    return None

def main():
    existing: dict[str, str | None] = {}
    if os.path.exists(OUTPUT):
        with open(OUTPUT, encoding="utf-8") as f:
            for entry in json.load(f):
                existing[entry["n"]] = entry.get("im")

    results = []
    for m in MINERALS:
        name = m["n"]
        if name in existing:
            image_url = existing[name]
            print(f"  [cache] {name}")
        else:
            wiki_title = WIKI_TITLE_OVERRIDES.get(name, name)
            image_url = fetch_wiki_image(wiki_title)
            if image_url is None:
                image_url = fetch_commons_image(wiki_title)
            status = "✓" if image_url else "✗"
            print(f"  [{status}] {name}: {image_url or 'no image'}")
            time.sleep(0.8)

        results.append({**m, "im": image_url})

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, separators=(",", ":"))
    print(f"\nWrote {len(results)} minerals → {OUTPUT}")

if __name__ == "__main__":
    main()
