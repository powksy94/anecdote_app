import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

FILES = {
    "assets/mythology/greek_mythology.json": "Greek mythology",
    "assets/mythology/norse_mythology.json": "Norse mythology",
    "assets/mythology/egyptian_mythology.json": "Egyptian mythology",
    "assets/mythology/mythological_creatures.json": "mythology",
}


def pageimage(title):
    try:
        url = ("https://en.wikipedia.org/w/api.php?action=query&prop=pageimages"
               "&format=json&titles=" + quote(title) + "&pithumbsize=500")
        r = requests.get(url, headers=HEADERS, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception:
        pass
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(title)
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            src = r.json().get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception:
        pass
    return None


def opensearch_candidates(query):
    try:
        url = ("https://en.wikipedia.org/w/api.php?action=opensearch&format=json"
               "&limit=5&namespace=0&search=" + quote(query))
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        return data[1] if len(data) > 1 else []
    except Exception:
        return []


def find_image(name, context):
    variants = [
        name,
        "{} (mythology)".format(name),
        "{} (deity)".format(name),
        "{} (god)".format(name),
        "{} (goddess)".format(name),
        "{} ({})".format(name, context),
    ]
    for v in variants:
        img = pageimage(v)
        time.sleep(0.2)
        if img:
            return img, v

    base = name.split(" (")[0]
    candidates = opensearch_candidates(base)
    for c in candidates:
        if base.lower() in c.lower():
            img = pageimage(c)
            time.sleep(0.2)
            if img:
                return img, c
    return None, None


def main():
    grand_before = 0
    grand_after = 0
    for path_str, context in FILES.items():
        path = Path(path_str)
        data = json.loads(path.read_text(encoding="utf-8"))
        missing = [x for x in data if not x.get("im")]
        grand_before += len(missing)
        recovered = 0
        for entry in missing:
            img, via = find_image(entry["n"], context)
            if img:
                entry["im"] = img
                recovered += 1
                sys.stdout.write("  ok  {} (via '{}')\n".format(entry["n"], via))
            else:
                sys.stdout.write("  xx  {}\n".format(entry["n"]))
            sys.stdout.flush()
        grand_after += recovered
        path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        sys.stdout.write("{}: recovered {}/{}\n\n".format(path_str, recovered, len(missing)))

    sys.stdout.write("TOTAL: recovered {}/{} missing images\n".format(grand_after, grand_before))


if __name__ == "__main__":
    main()
