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
    "False ribs (R8-R10)":           "False rib",
    "Floating ribs (R11-R12)":       "Floating rib",
    "Clavicle":                      "Clavicle",
    "Scapula":                       "Scapula",
    "Humerus":                       "Humerus",
    "Radius":                        "Radius (bone)",
    "Ulna":                          "Ulna",
    "Scaphoid":                      "Scaphoid bone",
    "Lunate":                        "Lunate bone",
    "Triquetrum":                    "Triquetrum bone",
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
    "Medial cuneiform":              "Medial cuneiform bone",
    "Intermediate cuneiform":        "Intermediate cuneiform bone",
    "Lateral cuneiform":             "Lateral cuneiform bone",
    "Metatarsal bones":              "Metatarsal bones",
    "Phalanges of foot":             "Phalanges of the foot",
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
    for bone in HUMAN_BONES:
        name = bone["n"]
        if name in existing_map and existing_map[name].get("im") is not None:
            print(f"  skip (cached)  {name}")
            result.append({**bone, "im": existing_map[name]["im"]})
            continue

        wiki_title = WIKI_TITLE_OVERRIDES.get(name, name)
        print(f"  fetch  {name}  →  {wiki_title}")
        image_url = fetch_wiki_image(wiki_title)
        result.append({**bone, "im": image_url})
        time.sleep(0.3)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {len(result)} bones → {OUTPUT}")

if __name__ == "__main__":
    main()

