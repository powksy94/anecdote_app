import json, requests, time, os, sys
sys.stdout.reconfigure(encoding="utf-8")

from insects_raw import INSECTS_RAW

HEADERS = {"User-Agent": "projet_app_annecdote/1.0 (daily-facts educational app; github.com/uzan)"}

def fetch_wiki_image(name, size=500):
    for attempt in range(3):
        if attempt > 0:
            time.sleep(2 ** attempt)
        try:
            r = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action":"query","titles":name,"prop":"pageimages",
                        "format":"json","pithumbsize":size},
                headers=HEADERS, timeout=12,
            )
            if not r.text.strip():
                continue
            pages = r.json()["query"]["pages"]
            page  = next(iter(pages.values()))
            return page.get("thumbnail", {}).get("source")
        except Exception:
            pass
    return None

def fetch_commons_image(query, size=500):
    try:
        r = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={"action":"query","generator":"search","gsrsearch":query,
                    "gsrnamespace":6,"prop":"imageinfo","iiprop":"url",
                    "iiurlwidth":size,"format":"json","gsrlimit":5},
            headers=HEADERS, timeout=15,
        )
        if not r.text.strip():
            return None
        pages = r.json().get("query", {}).get("pages", {})
        for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
            info = page.get("imageinfo", [])
            if info:
                url = info[0].get("thumburl") or info[0].get("url")
                if url and ".svg" not in url.lower():
                    return url
    except Exception:
        pass
    return None

output_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../assets/science/insects.json")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

existing_images = {}
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        for entry in json.load(f):
            if entry.get("im"):
                existing_images[entry["n"]] = entry["im"]
    print(f"Loaded {len(existing_images)} existing images from cache.\n")

missing = sum(1 for e in INSECTS_RAW if not existing_images.get(e["n"]))
print(f"{missing} insect(s) need image fetching.\n")
fetch_idx = 0
insects = []
for i, e in enumerate(INSECTS_RAW, 1):
    name = e["n"]
    if existing_images.get(name):
        im = existing_images[name]
        print(f"[{i:3}/{len(INSECTS_RAW)}] {name} (cached)")
    else:
        fetch_idx += 1
        print(f"[{i:3}/{len(INSECTS_RAW)}] Fetching image for {name} ...")
        im = fetch_wiki_image(name)
        if im is None:
            im = fetch_commons_image(f"{name} insect")
        if im is None:
            im = fetch_commons_image(name)
        if im:
            print(f"  found: {im[:80]}")
        if fetch_idx < missing:
            time.sleep(0.8)
    insects.append({**e, "im": im})

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(insects, f, ensure_ascii=False, separators=(",", ":"))

fetched = sum(1 for e in insects if e["im"])
print(f"\nDone -- {len(insects)} insects, {fetched} with images -> {output_path}")
