#!/usr/bin/env python3
"""Generate assets/science/human_bones.json — fetch images from Wikipedia/Wikimedia."""

import json, time, urllib.parse, urllib.request, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from human_bones_raw import HUMAN_BONES

OUTPUT = os.path.join(os.path.dirname(__file__), '../../assets/science/human_bones.json')

WIKI_TITLE_OVERRIDES = {
    "Frontal bone":                  "Frontal bone",
    "Parietal bone":                 "Parietal bone",
    "Temporal bone":                 "Temporal bone",
    "Occipital bone":                "Occipital bone",
    "Sphenoid bone":                 "Sphenoid bone",
    "Ethmoid bone":                  "Ethmoid bone",
    "Nasal bone":                    "Nasal bone",
    "Vomer":                         "Vomer",
    "Mandible":                      "Mandible",
    "Maxilla":                       "Maxilla",
    "Zygomatic bone":                "Zygomatic bone",
    "Lacrimal bone":                 "Lacrimal bone",
    "Palatine bone":                 "Palatine bone",
    "Inferior nasal concha":         "Inferior nasal concha",
    "Hyoid bone":                    "Hyoid bone",
    "Malleus":                       "Malleus",
    "Incus":                         "Incus",
    "Stapes":                        "Stapes",
    "Atlas (C1)":                    "Atlas (anatomy)",
    "Axis (C2)":                     "Axis (anatomy)",
    "Cervical vertebrae (C3-C7)":    "Cervical vertebrae",
    "Thoracic vertebrae (T1-T12)":   "Thoracic vertebrae",
    "Lumbar vertebrae (L1-L5)":      "Lumbar vertebrae",
    "Sacrum":                        "Sacrum",
    "Coccyx":                        "Coccyx",
    "Sternum":                       "Sternum",
    "True ribs (R1-R7)":             "Rib",
    "False ribs (R8-R10)":           "Rib cage",
    "Floating ribs (R11-R12)":       "Rib",
    "Clavicle":                      "Clavicle",
    "Scapula":                       "Scapula",
    "Humerus":                       "Humerus",
    "Radius":                        "Radius (bone)",
    "Ulna":                          "Ulna",
    "Scaphoid":                      "Scaphoid bone",
    "Lunate":                        "Lunate bone",
    "Triquetrum":                    "Triquetral bone",
    "Pisiform":                      "Pisiform bone",
    "Trapezium":                     "Trapezium (bone)",
    "Trapezoid":                     "Trapezoid bone",
    "Capitate":                      "Capitate bone",
    "Hamate":                        "Hamate bone",
    "Metacarpal bones":              "Metacarpal bones",
    "Phalanges of hand":             "Phalanges of the hand",
    "Ilium":                         "Ilium (bone)",
    "Ischium":                       "Ischium",
    "Pubis":                         "Pubis (bone)",
    "Femur":                         "Femur",
    "Patella":                       "Patella",
    "Tibia":                         "Tibia",
    "Fibula":                        "Fibula",
    "Calcaneus":                     "Calcaneus",
    "Talus":                         "Talus bone",
    "Navicular":                     "Navicular bone",
    "Cuboid":                        "Cuboid bone",
    "Medial cuneiform":              "Cuneiform bones",
    "Intermediate cuneiform":        "Cuneiform bones",
    "Lateral cuneiform":             "Cuneiform bones",
    "Metatarsal bones":              "Metatarsal bones",
    "Phalanges of foot":             "Phalanges of the foot",
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
        sys.stdout.buffer.write(f"  WARNING: {title} -- {e}\n".encode("utf-8")); sys.stdout.buffer.flush()
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
    for bone in HUMAN_BONES:
        name = bone["n"]
        if name in existing_map and existing_map[name].get("im") is not None:
            sys.stdout.buffer.write(f"  skip (cached)  {name}\n".encode("utf-8")); sys.stdout.buffer.flush()
            result.append({**bone, "im": existing_map[name]["im"]})
            continue

        wiki_title = WIKI_TITLE_OVERRIDES.get(name, name)
        sys.stdout.buffer.write(f"  fetch  {name}  ->  {wiki_title}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        image_url = fetch_wiki_image(wiki_title)
        if image_url is None:
            image_url = fetch_commons_image(f"{name} anatomy bone")
        if image_url is None:
            image_url = fetch_commons_image(name)
        result.append({**bone, "im": image_url})
        time.sleep(0.3)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    sys.stdout.buffer.write(f"\nWrote {len(result)} bones -> {OUTPUT}\n".encode("utf-8"))

if __name__ == "__main__":
    main()

