"""
Adds telescope/NASA images to stars.json.
Uses Wikimedia Commons imageinfo API (exact filename) for manual overrides,
Wikipedia pageimages API for stars where the API returns a real photo.
Skips stars where the API would return a constellation/IAU map.
Run from project root: py tools/space/add_images_stars.py
"""

import json, requests, sys, time
from pathlib import Path
from urllib.parse import quote

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Stars with known exact Commons filenames (real telescope/NASA/ESA images).
# The Commons imageinfo API converts the filename to the actual thumb URL.
COMMONS_FILES = {
    "Betelgeuse":        "Hubble Sees Red Supergiant Star Betelgeuse Slowly Recovering After Blowing Its Top (opo22037a).jpg",
    "Sirius A":          "Sirius_A_and_B_Hubble_photo.editted.PNG",
    "Eta Carinae":       "Eta Carinae Nebula 1.jpg",
    "V838 Monocerotis":  "V838 Mon HST.jpg",
    "Mira":              "Mira the star-by Nasa alt crop.jpg",
    "Fomalhaut":         "Fomalhaut_with_Disk_Ring_and_extrasolar_planet_b.jpg",
    "Beta Pictoris":     "Circumstellar Disk Around Beta Pictoris (opo9803a).jpg",
    "Cygnus X-1":        "Chandra_image_of_Cygnus_X-1.jpg",
    "KIC 8462852":       "KIC 8462852 in IR and UV.png",
}

# Stars where Wikipedia pageimages API returns a real photo (not a map).
# Verified by checking the returned URL doesn't contain "constellation" / "IAU".
ALLOWLIST_WIKI = {
    "Sun":                "Sun",
    "Proxima Centauri":   "Proxima Centauri",
    "TRAPPIST-1":         "TRAPPIST-1",
    "VY Canis Majoris":   "VY Canis Majoris",
    "UY Scuti":           "UY Scuti",
    "Pistol Star":        "Pistol Star",
    "R136a1":             "R136a1",
    "HR 8799":            "HR 8799",
    "WR 104":             "WR 104",
}

# Keywords that flag a bad image (constellation maps, SVG diagrams, etc.)
BAD_IMAGE_KEYWORDS = [
    "constellation", "IAU", "_map", "location", "finder",
    ".svg", "chart", "TCrBLocation",
]


def is_bad_image(url: str) -> bool:
    return any(kw.lower() in url.lower() for kw in BAD_IMAGE_KEYWORDS)


def commons_thumb(filename: str, width: int = 480) -> str | None:
    """Get thumbnail URL from Wikimedia Commons by exact filename."""
    url = (
        "https://commons.wikimedia.org/w/api.php"
        f"?action=query&titles=File:{quote(filename)}"
        f"&prop=imageinfo&iiprop=url&iiurlwidth={width}&format=json"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            infos = page.get("imageinfo", [])
            if infos:
                return infos[0].get("thumburl") or infos[0].get("url")
    except Exception as e:
        sys.stdout.buffer.write(f"    commons error: {e}\n".encode("utf-8"))
    return None


def wiki_img(title: str) -> str | None:
    """Get thumbnail from Wikipedia pageimages API, reject constellation maps."""
    api_url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=query&prop=pageimages&format=json"
        f"&titles={quote(title)}&pithumbsize=500"
    )
    try:
        r = requests.get(api_url, headers=HEADERS, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("thumbnail", {}).get("source")
            if src and not is_bad_image(src):
                return src
    except Exception:
        pass
    return None


def main():
    json_path = Path("assets/space/stars.json")
    stars = json.loads(json_path.read_text(encoding="utf-8-sig"))
    total = len(stars)
    found = 0

    for i, s in enumerate(stars):
        name = s["n"]

        if name in COMMONS_FILES:
            img = commons_thumb(COMMONS_FILES[name])
            s["im"] = img
            if img:
                found += 1
            status = "commons ok" if img else "commons NONE"
            sys.stdout.buffer.write(f"  [{i+1:3}/{total}] {status} {name}\n".encode("utf-8"))
            sys.stdout.buffer.flush()
            time.sleep(0.3)
            continue

        if name in ALLOWLIST_WIKI:
            img = wiki_img(ALLOWLIST_WIKI[name])
            s["im"] = img
            if img:
                found += 1
            status = "wiki ok  " if img else "wiki NONE"
            sys.stdout.buffer.write(f"  [{i+1:3}/{total}] {status} {name}\n".encode("utf-8"))
            sys.stdout.buffer.flush()
            time.sleep(0.3)
            continue

        s["im"] = None
        sys.stdout.buffer.write(f"  [{i+1:3}/{total}] skip     {name}\n".encode("utf-8"))
        sys.stdout.buffer.flush()

    json_path.write_text(
        json.dumps(stars, ensure_ascii=False, separators=(',', ':')),
        encoding="utf-8"
    )
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images.\n".encode("utf-8"))


if __name__ == "__main__":
    main()
