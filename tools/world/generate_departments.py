import json, requests, time, sys
sys.stdout.reconfigure(encoding="utf-8")

# geo.api.gouv.fr - liste des départements
depts = requests.get(
    "https://geo.api.gouv.fr/departements?fields=nom,code,region"
).json()

# Données population + superficie (source INSEE 2021)
insee = {
    "01":{"po":649110,"ar":5762},"02":{"po":534490,"ar":7369},
    "03":{"po":337988,"ar":7340},"04":{"po":165197,"ar":6925},
    "05":{"po":141521,"ar":5549},"06":{"po":1094369,"ar":4299},
    "07":{"po":340432,"ar":5529},"08":{"po":272579,"ar":5229},
    "09":{"po":153153,"ar":4890},"10":{"po":310020,"ar":6004},
    "11":{"po":374071,"ar":6139},"12":{"po":279206,"ar":8735},
    "13":{"po":2055697,"ar":5087},"14":{"po":694856,"ar":5548},
    "15":{"po":144589,"ar":5726},"16":{"po":352705,"ar":5956},
    "17":{"po":655506,"ar":6864},"18":{"po":303600,"ar":7235},
    "19":{"po":241464,"ar":5888},"2A":{"po":161576,"ar":4014},
    "2B":{"po":184074,"ar":4666},"21":{"po":534610,"ar":8765},
    "22":{"po":608007,"ar":6878},"23":{"po":115668,"ar":5565},
    "24":{"po":413797,"ar":9060},"25":{"po":545959,"ar":5234},
    "26":{"po":519866,"ar":6530},"27":{"po":601843,"ar":6040},
    "28":{"po":440916,"ar":5880},"29":{"po":906538,"ar":6733},
    "30":{"po":748437,"ar":5853},"31":{"po":1399762,"ar":6309},
    "32":{"po":195167,"ar":6257},"33":{"po":1623749,"ar":9976},
    "34":{"po":1155447,"ar":6101},"35":{"po":1096722,"ar":6775},
    "36":{"po":221742,"ar":6791},"37":{"po":611620,"ar":6127},
    "38":{"po":1271166,"ar":7431},"39":{"po":261479,"ar":4999},
    "40":{"po":416645,"ar":9243},"41":{"po":337451,"ar":6343},
    "42":{"po":764074,"ar":4781},"43":{"po":229574,"ar":4977},
    "44":{"po":1429272,"ar":6815},"45":{"po":685103,"ar":6775},
    "46":{"po":183083,"ar":5217},"47":{"po":340088,"ar":5361},
    "48":{"po":75832,"ar":5167},"49":{"po":806727,"ar":7166},
    "50":{"po":495042,"ar":5938},"51":{"po":568895,"ar":8162},
    "52":{"po":172206,"ar":6211},"53":{"po":307530,"ar":5175},
    "54":{"po":733481,"ar":5246},"55":{"po":184286,"ar":6211},
    "56":{"po":761618,"ar":6823},"57":{"po":1042590,"ar":6216},
    "58":{"po":204194,"ar":6817},"59":{"po":2608280,"ar":5743},
    "60":{"po":833765,"ar":5860},"61":{"po":277073,"ar":6144},
    "62":{"po":1467253,"ar":6671},"63":{"po":667456,"ar":7970},
    "64":{"po":692611,"ar":7645},"65":{"po":224139,"ar":4464},
    "66":{"po":481603,"ar":4116},"67":{"po":1145590,"ar":4755},
    "68":{"po":765634,"ar":3525},"69":{"po":1843375,"ar":3249},
    "70":{"po":234752,"ar":5360},"71":{"po":553988,"ar":8575},
    "72":{"po":568654,"ar":6206},"73":{"po":438490,"ar":6028},
    "74":{"po":832264,"ar":4388},"75":{"po":2102650,"ar":105},
    "76":{"po":1270442,"ar":6278},"77":{"po":1422594,"ar":5915},
    "78":{"po":1446789,"ar":2284},"79":{"po":382258,"ar":5999},
    "80":{"po":572443,"ar":6170},"81":{"po":393857,"ar":5758},
    "82":{"po":260629,"ar":3718},"83":{"po":1079670,"ar":5973},
    "84":{"po":560223,"ar":3567},"85":{"po":685442,"ar":6720},
    "86":{"po":437764,"ar":6990},"87":{"po":373258,"ar":5520},
    "88":{"po":366498,"ar":5874},"89":{"po":338291,"ar":7427},
    "90":{"po":163190,"ar":609},"91":{"po":1296130,"ar":1804},
    "92":{"po":1609306,"ar":176},"93":{"po":1626230,"ar":236},
    "94":{"po":1387926,"ar":245},"95":{"po":1252511,"ar":1246},
    # DOM
    "971":{"po":395700,"ar":1628},"972":{"po":349925,"ar":1128},
    "973":{"po":294071,"ar":83534},"974":{"po":895312,"ar":2512},
    "976":{"po":371001,"ar":374},
}

# Préfectures
prefectures = {
    "01":"Bourg-en-Bresse","02":"Laon","03":"Moulins","04":"Digne-les-Bains",
    "05":"Gap","06":"Nice","07":"Privas","08":"Charleville-Mézières",
    "09":"Foix","10":"Troyes","11":"Carcassonne","12":"Rodez",
    "13":"Marseille","14":"Caen","15":"Aurillac","16":"Angoulême",
    "17":"La Rochelle","18":"Bourges","19":"Tulle","2A":"Ajaccio",
    "2B":"Bastia","21":"Dijon","22":"Saint-Brieuc","23":"Guéret",
    "24":"Périgueux","25":"Besançon","26":"Valence","27":"Évreux",
    "28":"Chartres","29":"Quimper","30":"Nîmes","31":"Toulouse",
    "32":"Auch","33":"Bordeaux","34":"Montpellier","35":"Rennes",
    "36":"Châteauroux","37":"Tours","38":"Grenoble","39":"Lons-le-Saunier",
    "40":"Mont-de-Marsan","41":"Blois","42":"Saint-Étienne","43":"Le Puy-en-Velay",
    "44":"Nantes","45":"Orléans","46":"Cahors","47":"Agen",
    "48":"Mende","49":"Angers","50":"Saint-Lô","51":"Châlons-en-Champagne",
    "52":"Chaumont","53":"Laval","54":"Nancy","55":"Bar-le-Duc",
    "56":"Vannes","57":"Metz","58":"Nevers","59":"Lille",
    "60":"Beauvais","61":"Alençon","62":"Arras","63":"Clermont-Ferrand",
    "64":"Pau","65":"Tarbes","66":"Perpignan","67":"Strasbourg",
    "68":"Colmar","69":"Lyon","70":"Vesoul","71":"Mâcon",
    "72":"Le Mans","73":"Chambéry","74":"Annecy","75":"Paris",
    "76":"Rouen","77":"Melun","78":"Versailles","79":"Niort",
    "80":"Amiens","81":"Albi","82":"Montauban","83":"Toulon",
    "84":"Avignon","85":"La Roche-sur-Yon","86":"Poitiers","87":"Limoges",
    "88":"Épinal","89":"Auxerre","90":"Belfort","91":"Évry-Courcouronnes",
    "92":"Nanterre","93":"Bobigny","94":"Créteil","95":"Cergy",
    "971":"Basse-Terre","972":"Fort-de-France","973":"Cayenne",
    "974":"Saint-Denis","976":"Mamoudzou",
}

result = []
for d in depts:
    code = d["code"]
    data = insee.get(code, {})
    result.append({
        "co":   code,
        "n":    d["nom"],
        "pr":   prefectures.get(code, ""),
        "re":   d.get("region", {}).get("nom", ""),
        "po":   data.get("po"),
        "ar":   data.get("ar"),
    })
    print(f"    {code} - {d['nom']} ✓")

with open("assets/world/french_departments.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

print(f"\n{len(result)} départements générés.")