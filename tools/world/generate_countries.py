import json, requests, time

# --- REST Countries : États souverains uniquement ---
rc = requests.get("https://restcountries.com/v3.1/independent?status=true&fields=name,cca2,cca3,capital,region,area,population,currencies,languages").json()

# Index par ISO2
by_iso2 = {}
for c in rc:
    iso2 = c.get("cca2", "")
    if not iso2:
        continue
    currencies = c.get("currencies", {})
    cur = {}
    if currencies:
        code = next(iter(currencies))
        cur = {"code": code, "name": currencies[code].get("name",""), "symbol": currencies[code].get("symbol","")}
    langages = list(c.get("languages", {}).values())
    by_iso2[iso2] = {
        "n":    c["name"]["common"],
        "i2":   iso2,
        "ca":   (c.get("capital") or [""])[0],
        "re":   c.get("region", ""),
        "ar":   c.get("area"),
        "po":   c.get("population"),
        "cu":   cur,
        "la":   langages,
    }

# --- World Bank : espérance de vie + chômage ---
WB_BASE = "https://api.worldbank.org/v2/country/{iso2}/indicator/{ind}?format=json&mrv=1"

def wb_value(iso2, indicator):
    try:
        r = requests.get(WB_BASE.format(iso2=iso2, ind=indicator), timeout=10).json()
        entries = r[1] if len(r) > 1 else []
        for e in entries:
            if e.get("value") is not None:
                return e["value"]
    except:
        pass
    return None

# --- IMF : PIB 2024 ---
imf_url = "https://www.imf.org/external/datamapper/api/v1/NGDPD"
imf_data = {}
try:
    r = requests.get(imf_url, timeout=15).json()
    values = r.get("values", {}).get("NGDPD", {})
    for iso3, years in values.items():
        if years:
            latest_year = max(years.keys())
            imf_data[iso3.upper()] = years[latest_year]  # en milliards USD
except:
    pass

# Table ISO2 -> ISO3 via REST Countries
iso2_to_iso3 = {}
for c in rc:
    iso2_to_iso3[c.get("cca2","")] = c.get("cca3","")

# --- Fusion ---
result = []
for iso2, country in by_iso2.items():
    time.sleep(0.1) # éviter rate limit World Bank
    country["le"] = wb_value(iso2, "SP.DYN.LE00.IN")
    country["un"] = wb_value(iso2, "SL.UEM.TOTL.ZS")
    iso3 = iso2_to_iso3.get(iso2, "")
    country["gd"] = imf_data.get(iso3) # milliards USD
    result.append(country)
    print(f"    {country['n']} ✓")

with open("assets/countries.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

print(f"\n{len(result)} pays générés.")