import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# Légende des champs
# n=name, pl=planet, di=diameter, op=orbital period, dy=discovery year
# dc=discoverer, fe=features
# im = image_url (Wikipedia/NASA thumbnail, null si introuvable)

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Titres Wikipedia EN — beaucoup de lunes ont besoin de disambiguation "(moon)"
WIKI_EN = {
    "Moon":        "Moon",
    "Phobos":      "Phobos (moon)",
    "Deimos":      "Deimos (moon)",
    "Io":          "Io (moon)",
    "Europa":      "Europa (moon)",
    "Ganymede":    "Ganymede (moon)",
    "Callisto":    "Callisto (moon)",
    "Amalthea":    "Amalthea (moon)",
    "Thebe":       "Thebe (moon)",
    "Metis":       "Metis (moon)",
    "Himalia":     "Himalia (moon)",
    "Elara":       "Elara (moon)",
    "Pasiphae":    "Pasiphae (moon)",
    "Titan":       "Titan (moon)",
    "Enceladus":   "Enceladus (moon)",
    "Mimas":       "Mimas (moon)",
    "Tethys":      "Tethys (moon)",
    "Dione":       "Dione (moon)",
    "Rhea":        "Rhea (moon)",
    "Iapetus":     "Iapetus (moon)",
    "Hyperion":    "Hyperion (moon)",
    "Phoebe":      "Phoebe (moon)",
    "Janus":       "Janus (moon)",
    "Epimetheus":  "Epimetheus (moon)",
    "Helene":      "Helene (moon)",
    "Atlas":       "Atlas (moon)",
    "Prometheus":  "Prometheus (moon)",
    "Pandora":     "Pandora (moon)",
    "Pan":         "Pan (moon)",
    "Calypso":     "Calypso (moon)",
    "Titania":     "Titania (moon)",
    "Oberon":      "Oberon (moon)",
    "Umbriel":     "Umbriel (moon)",
    "Ariel":       "Ariel (moon)",
    "Miranda":     "Miranda (moon)",
    "Puck":        "Puck (moon)",
    "Sycorax":     "Sycorax (moon)",
    "Caliban":     "Caliban (moon)",
    "Triton":      "Triton (moon)",
    "Nereid":      "Nereid (moon)",
    "Proteus":     "Proteus (moon)",
    "Larissa":     "Larissa (moon)",
    "Galatea":     "Galatea (moon)",
    "Despina":     "Despina (moon)",
    "Charon":      "Charon (moon)",
    "Nix":         "Nix (moon)",
    "Hydra":       "Hydra (moon)",
    "Kerberos":    "Kerberos (moon)",
    "Styx":        "Styx (moon)",
    "Dysnomia":    "Dysnomia (moon)",
    "Hi'iaka":     "Hiʻiaka (moon)",
    "Namaka":      "Namaka (moon)",
    "MK2":         "MK 2 (moon)",
}

def wiki_img(title: str) -> str | None:
    url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=query&prop=pageimages&format=json"
        f"&titles={quote(title)}&pithumbsize=500"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception:
        pass
    try:
        rest_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
        r = requests.get(rest_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            src = r.json().get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception:
        pass
    return None

def main():
    json_path = Path("assets/space/solar_moons.json")
    moons = json.loads(json_path.read_text(encoding="utf-8"))
    total = len(moons)
    found = 0

    for i, m in enumerate(moons):
        name = m["n"]
        title = WIKI_EN.get(name, name)
        img = wiki_img(title)
        m["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {name} ({m['pl']})\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    json_path.write_text(
        json.dumps(moons, ensure_ascii=False, separators=(',', ':')),
        encoding="utf-8"
    )
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images.\n".encode("utf-8"))

if __name__ == "__main__":
    main()
