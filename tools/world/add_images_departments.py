import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# Légende des champs
# co = code, n = name, pr = prefecture, re = region
# po = population, ar = area km²
# im = image_url (blason/emblème Wikipedia, null si introuvable)

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Titres fr.wikipedia.org — la plupart correspondent au nom du département
FR_WIKI = {
    "Ain":                      "Ain",
    "Aisne":                    "Aisne",
    "Allier":                   "Allier (département)",
    "Alpes-de-Haute-Provence":  "Alpes-de-Haute-Provence",
    "Hautes-Alpes":             "Hautes-Alpes",
    "Alpes-Maritimes":          "Alpes-Maritimes",
    "Ardèche":                  "Ardèche (département)",
    "Ardennes":                 "Ardennes (département)",
    "Ariège":                   "Ariège (département)",
    "Aube":                     "Aube (département)",
    "Aude":                     "Aude (département)",
    "Aveyron":                  "Aveyron (département)",
    "Bouches-du-Rhône":         "Bouches-du-Rhône",
    "Calvados":                 "Calvados (département)",
    "Cantal":                   "Cantal (département)",
    "Charente":                 "Charente (département)",
    "Charente-Maritime":        "Charente-Maritime",
    "Cher":                     "Cher (département)",
    "Corrèze":                  "Corrèze (département)",
    "Côte-d'Or":                "Côte-d'Or",
    "Côtes-d'Armor":            "Côtes-d'Armor",
    "Creuse":                   "Creuse (département)",
    "Dordogne":                 "Dordogne (département)",
    "Doubs":                    "Doubs (département)",
    "Drôme":                    "Drôme (département)",
    "Eure":                     "Eure (département)",
    "Eure-et-Loir":             "Eure-et-Loir",
    "Finistère":                "Finistère",
    "Corse-du-Sud":             "Corse-du-Sud",
    "Haute-Corse":              "Haute-Corse",
    "Gard":                     "Gard (département)",
    "Haute-Garonne":            "Haute-Garonne",
    "Gers":                     "Gers (département)",
    "Gironde":                  "Gironde (département)",
    "Hérault":                  "Hérault (département)",
    "Ille-et-Vilaine":          "Ille-et-Vilaine",
    "Indre":                    "Indre (département)",
    "Indre-et-Loire":           "Indre-et-Loire",
    "Isère":                    "Isère (département)",
    "Jura":                     "Jura (département)",
    "Landes":                   "Landes (département)",
    "Loir-et-Cher":             "Loir-et-Cher",
    "Loire":                    "Loire (département)",
    "Haute-Loire":              "Haute-Loire",
    "Loire-Atlantique":         "Loire-Atlantique",
    "Loiret":                   "Loiret",
    "Lot":                      "Lot (département)",
    "Lot-et-Garonne":           "Lot-et-Garonne",
    "Lozère":                   "Lozère (département)",
    "Maine-et-Loire":           "Maine-et-Loire",
    "Manche":                   "Manche (département)",
    "Marne":                    "Marne (département)",
    "Haute-Marne":              "Haute-Marne",
    "Mayenne":                  "Mayenne (département)",
    "Meurthe-et-Moselle":       "Meurthe-et-Moselle",
    "Meuse":                    "Meuse (département)",
    "Morbihan":                 "Morbihan",
    "Moselle":                  "Moselle (département)",
    "Nièvre":                   "Nièvre",
    "Nord":                     "Nord (département)",
    "Oise":                     "Oise (département)",
    "Orne":                     "Orne (département)",
    "Pas-de-Calais":            "Pas-de-Calais",
    "Puy-de-Dôme":              "Puy-de-Dôme",
    "Pyrénées-Atlantiques":     "Pyrénées-Atlantiques",
    "Hautes-Pyrénées":          "Hautes-Pyrénées",
    "Pyrénées-Orientales":      "Pyrénées-Orientales",
    "Bas-Rhin":                 "Bas-Rhin",
    "Haut-Rhin":                "Haut-Rhin",
    "Rhône":                    "Rhône (département)",
    "Haute-Saône":              "Haute-Saône",
    "Saône-et-Loire":           "Saône-et-Loire",
    "Sarthe":                   "Sarthe (département)",
    "Savoie":                   "Savoie (département)",
    "Haute-Savoie":             "Haute-Savoie",
    "Paris":                    "Paris",
    "Seine-Maritime":           "Seine-Maritime",
    "Seine-et-Marne":           "Seine-et-Marne",
    "Yvelines":                 "Yvelines",
    "Deux-Sèvres":              "Deux-Sèvres",
    "Somme":                    "Somme (département)",
    "Tarn":                     "Tarn (département)",
    "Tarn-et-Garonne":          "Tarn-et-Garonne",
    "Var":                      "Var (département)",
    "Vaucluse":                 "Vaucluse (département)",
    "Vendée":                   "Vendée",
    "Vienne":                   "Vienne (département)",
    "Haute-Vienne":             "Haute-Vienne",
    "Vosges":                   "Vosges (département)",
    "Yonne":                    "Yonne (département)",
    "Territoire de Belfort":    "Territoire de Belfort",
    "Essonne":                  "Essonne (département)",
    "Hauts-de-Seine":           "Hauts-de-Seine",
    "Seine-Saint-Denis":        "Seine-Saint-Denis",
    "Val-de-Marne":             "Val-de-Marne",
    "Val-d'Oise":               "Val-d'Oise",
    "Guadeloupe":               "Guadeloupe",
    "Martinique":               "Martinique",
    "Guyane":                   "Guyane",
    "La Réunion":               "La Réunion",
    "Mayotte":                  "Mayotte",
}


def commons_thumb(file_title: str, width: int = 300) -> str | None:
    """Get thumbnail URL for a Wikimedia Commons file."""
    url = (
        "https://commons.wikimedia.org/w/api.php"
        f"?action=query&titles={quote(file_title)}"
        "&prop=imageinfo&iiprop=url"
        f"&iiurlwidth={width}&format=json"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            if page.get("pageid", -1) == -1:
                return None
            ii = page.get("imageinfo", [])
            if ii:
                return ii[0].get("thumburl")
    except Exception:
        pass
    return None


def get_blason_from_wiki(dept_name: str) -> str | None:
    """Scan fr.wikipedia.org page for a 'blason' image, then get its Commons thumbnail."""
    title = FR_WIKI.get(dept_name, dept_name)
    url = (
        "https://fr.wikipedia.org/w/api.php"
        "?action=query&prop=images&format=json"
        f"&titles={quote(title)}&imlimit=50"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            for img in page.get("images", []):
                img_title = img.get("title", "")
                lower = img_title.lower()
                if "blason" in lower or "armoiries" in lower or "coat" in lower:
                    # Normalize: "Fichier:" → "File:"
                    file_title = img_title.replace("Fichier:", "File:")
                    thumb = commons_thumb(file_title, width=300)
                    if thumb:
                        return thumb
    except Exception:
        pass
    return None


def wiki_pageimage(lang: str, title: str) -> str | None:
    """Fallback: main representative image of the Wikipedia article."""
    url = (
        f"https://{lang}.wikipedia.org/w/api.php"
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
    return None


def fetch_dept_image(dept_name: str) -> str | None:
    # 1. Chercher le blason sur fr.wikipedia
    img = get_blason_from_wiki(dept_name)
    if img:
        return img
    # 2. Fallback : image principale de l'article fr.wikipedia
    title = FR_WIKI.get(dept_name, dept_name)
    return wiki_pageimage("fr", title)


def main():
    json_path = Path("assets/world/french_departments.json")
    depts = json.loads(json_path.read_text(encoding="utf-8"))
    total = len(depts)
    found = 0

    for i, d in enumerate(depts):
        name = d["n"]
        img = fetch_dept_image(name)
        d["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:3}/{total}] {status} {name}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.4)  # légèrement plus lent (2 requêtes potentielles)

    json_path.write_text(
        json.dumps(depts, ensure_ascii=False, separators=(',', ':')),
        encoding="utf-8"
    )
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images.\n".encode("utf-8"))

if __name__ == "__main__":
    main()
