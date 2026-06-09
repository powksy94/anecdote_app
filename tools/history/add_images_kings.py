import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# Légende des champs
# n  = name, dy = dynasty, rs = reign start, re = reign end
# ni = nickname, fa = famous for
# im = image_url (Wikipedia portrait thumbnail, null si introuvable)

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Wikipedia EN article titles, keyed by (name, reignStart) pour éviter les doublons
WIKI_EN = {
    ("Clovis I",          481):  "Clovis I",
    ("Clotaire I",        511):  "Chlothar I",
    ("Chilpéric I",       561):  "Chilperic I",
    ("Dagobert I",        629):  "Dagobert I",
    ("Childéric III",     743):  "Childeric III",
    ("Pépin le Bref",     751):  "Pepin the Short",
    ("Charlemagne",       768):  "Charlemagne",
    ("Louis I",           814):  "Louis the Pious",
    ("Charles II",        843):  "Charles the Bald",
    ("Louis II",          877):  "Louis the Stammerer",
    ("Louis III",         879):  "Louis III of France",
    ("Carloman II",       879):  "Carloman II",
    ("Charles III",       884):  "Charles the Fat",
    ("Eudes",             888):  "Odo of France",
    ("Charles III",       898):  "Charles the Simple",
    ("Robert I",          922):  "Robert I of France",
    ("Raoul",             923):  "Raoul of France",
    ("Louis IV",          936):  "Louis IV of France",
    ("Lothaire",          954):  "Lothair of France",
    ("Louis V",           986):  "Louis V of France",
    ("Hugues Capet",      987):  "Hugh Capet",
    ("Robert II",         996):  "Robert II of France",
    ("Henri I",          1031):  "Henry I of France",
    ("Philippe I",       1060):  "Philip I of France",
    ("Louis VI",         1108):  "Louis VI of France",
    ("Louis VII",        1137):  "Louis VII of France",
    ("Philippe II",      1180):  "Philip II of France",
    ("Louis VIII",       1223):  "Louis VIII of France",
    ("Louis IX",         1226):  "Louis IX of France",
    ("Philippe III",     1270):  "Philip III of France",
    ("Philippe IV",      1285):  "Philip IV of France",
    ("Louis X",          1314):  "Louis X of France",
    ("Philippe V",       1316):  "Philip V of France",
    ("Charles IV",       1322):  "Charles IV of France",
    ("Philippe VI",      1328):  "Philip VI of France",
    ("Jean II",          1350):  "John II of France",
    ("Charles V",        1364):  "Charles V of France",
    ("Charles VI",       1380):  "Charles VI of France",
    ("Charles VII",      1422):  "Charles VII of France",
    ("Louis XI",         1461):  "Louis XI of France",
    ("Charles VIII",     1483):  "Charles VIII of France",
    ("Louis XII",        1498):  "Louis XII of France",
    ("François I",       1515):  "Francis I of France",
    ("Henri II",         1547):  "Henry II of France",
    ("François II",      1559):  "Francis II of France",
    ("Charles IX",       1560):  "Charles IX of France",
    ("Henri III",        1574):  "Henry III of France",
    ("Henri IV",         1589):  "Henry IV of France",
    ("Louis XIII",       1610):  "Louis XIII",
    ("Louis XIV",        1643):  "Louis XIV of France",
    ("Louis XV",         1715):  "Louis XV of France",
    ("Louis XVI",        1774):  "Louis XVI",
    ("Louis XVIII",      1814):  "Louis XVIII of France",
    ("Charles X",        1824):  "Charles X of France",
    ("Louis-Philippe I", 1830):  "Louis-Philippe I",
}

def wiki_img(title: str) -> str | None:
    # 1. MediaWiki API prop=pageimages
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
    # 2. Fallback: Wikimedia REST summary (more reliable for articles with paintings)
    try:
        rest_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
        r = requests.get(rest_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            src = data.get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception:
        pass
    return None

def main():
    json_path = Path("assets/history/kings_of_france.json")
    kings = json.loads(json_path.read_text(encoding="utf-8"))
    total = len(kings)
    found = 0

    for i, k in enumerate(kings):
        key = (k["n"], k["rs"])
        title = WIKI_EN.get(key, k["n"])
        img = wiki_img(title)
        k["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {k['n']}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    json_path.write_text(
        json.dumps(kings, ensure_ascii=False, separators=(',', ':')),
        encoding="utf-8"
    )
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images.\n".encode("utf-8"))

if __name__ == "__main__":
    main()
