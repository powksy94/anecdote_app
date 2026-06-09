import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# Légende des champs
# n  = name, nu = number, mn = mandate number, ts = term start, te = term end
# pa = party, st = state, vp = vice president, fa = famous for
# im = image_url (Wikipedia portrait thumbnail, null si introuvable)

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Overrides pour les noms dont le titre Wikipedia diffère légèrement
WIKI_EN = {
    "George H.W. Bush": "George H. W. Bush",
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
    json_path = Path("assets/history/american_presidents.json")
    presidents = json.loads(json_path.read_text(encoding="utf-8"))

    # Cache par nom pour éviter de fetcher plusieurs fois la même personne
    img_cache: dict[str, str | None] = {}
    total = len(presidents)
    found = 0

    for i, p in enumerate(presidents):
        name = p["n"]
        if name not in img_cache:
            title = WIKI_EN.get(name, name)
            img_cache[name] = wiki_img(title)
            time.sleep(0.3)
        img = img_cache[name]
        p["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        mn_label = f" (mandate {p['mn']})" if p.get("mn") else ""
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {name}{mn_label}\n".encode("utf-8"))
        sys.stdout.buffer.flush()

    json_path.write_text(
        json.dumps(presidents, ensure_ascii=False, separators=(',', ':')),
        encoding="utf-8"
    )
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images.\n".encode("utf-8"))

if __name__ == "__main__":
    main()
