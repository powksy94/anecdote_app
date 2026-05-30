import json, requests, time, pathlib, sys

# Légende des champs (format compact)
# n  = name (nom de la commune)
# de = département (nom + numéro)
# rg = région administrative
# po = population (habitants)
# ar = area km² (superficie)
# fa = famous for (anecdote principale, en anglais)
# im = image_url (Wikipedia thumbnail, null si introuvable)

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Titres Wikipedia EN alternatifs (quand le titre de l'article diffère du nom)
WIKI_EN = {
    "Mont-Saint-Michel":        "Mont Saint-Michel",
    "Carnac":                   "Carnac, Morbihan",
    "Cherbourg-en-Cotentin":    "Cherbourg-en-Cotentin",
    "Corte":                    "Corte, Haute-Corse",
    "Saint-Pierre":             "Saint-Pierre, Martinique",
    "Chamonix":                 "Chamonix-Mont-Blanc",
    "Bourg-en-Bresse":          "Bourg-en-Bresse",
    "Bayeux":                   "Bayeux, Calvados",
    "Arras":                    "Arras, Pas-de-Calais",
    "Dinan":                    "Dinan, Côtes-d'Armor",
    "Senlis":                   "Senlis, Oise",
    "Verdun":                   "Verdun, Meuse",
    "Belfort":                  "Belfort",
    "Domrémy-la-Pucelle":       "Domrémy-la-Pucelle",
    "Orange":                   "Orange, Vaucluse",
    "Gap":                      "Gap, Hautes-Alpes",
    "Bar-le-Duc":               "Bar-le-Duc",
    "Rocroi":                   "Rocroi",
    "Laval":                    "Laval, Mayenne",
    "Laon":                     "Laon",
    "Moissac":                  "Moissac, Tarn-et-Garonne",
    "Mâcon":                    "Mâcon",
    "Nevers":                   "Nevers",
    "Cluny":                    "Cluny, Saône-et-Loire",
    "Semur-en-Auxois":          "Semur-en-Auxois",
    "Obernai":                  "Obernai",
    "Riquewihr":                "Riquewihr",
    "Figeac":                   "Figeac",
    "Mende":                    "Mende, Lozère",
    "Thiers":                   "Thiers, Puy-de-Dôme",
    "Draguignan":               "Draguignan",
    "Grasse":                   "Grasse",
    "Hyères":                   "Hyères",
    "Briançon":                 "Briançon",
    "Sisteron":                 "Sisteron",
    "La Ciotat":                "La Ciotat",
    "Uzès":                     "Uzès",
    "Millau":                   "Millau",
    "Narbonne":                 "Narbonne",
    "Collioure":                "Collioure",
    "Tulle":                    "Tulle, Corrèze",
    "Bergerac":                 "Bergerac, Dordogne",
    "Rochefort":                "Rochefort, Charente-Maritime",
    "Niort":                    "Niort",
    "Limoges":                  "Limoges",
    "Saint-Émilion":            "Saint-Émilion",
    "Saintes":                  "Saintes, Charente-Maritime",
    "Concarneau":               "Concarneau",
    "Pont-Aven":                "Pont-Aven",
    "Guérande":                 "Guérande",
    "Quiberon":                 "Quiberon",
    "Chinon":                   "Chinon, Indre-et-Loire",
    "Azay-le-Rideau":           "Azay-le-Rideau",
    "Loches":                   "Loches, Indre-et-Loire",
    "Vichy":                    "Vichy",
    "Épinal":                   "Épinal",
    "Moustiers-Sainte-Marie":   "Moustiers-Sainte-Marie",
    "Évian-les-Bains":          "Évian-les-Bains",
    "Grasse":                   "Grasse",
    "Éze":                      "Èze",
    "Melun":                    "Melun",
    "Nanterre":                 "Nanterre",
    "Chantilly":                "Chantilly, Oise",
    "Honfleur":                 "Honfleur",
    "Étretat":                  "Étretat",
    "Alençon":                  "Alençon",
}

# Titres Wikipedia FR (fallback si pas d'image en EN)
WIKI_FR = {
    "Orange":                   "Orange (Vaucluse)",
    "Gap":                      "Gap (Hautes-Alpes)",
    "Laval":                    "Laval (Mayenne)",
    "Mende":                    "Mende (Lozère)",
    "Cluny":                    "Cluny (Saône-et-Loire)",
    "Saint-Denis":              "Saint-Denis (La Réunion)",
    "Tulle":                    "Tulle (Corrèze)",
    "Bergerac":                 "Bergerac (Dordogne)",
    "Rochefort":                "Rochefort (Charente-Maritime)",
    "Thiers":                   "Thiers (Puy-de-Dôme)",
    "Chinon":                   "Chinon (Indre-et-Loire)",
    "Loches":                   "Loches (Indre-et-Loire)",
    "Saintes":                  "Saintes (Charente-Maritime)",
}

def _wiki_img(lang: str, title: str) -> str | None:
    url = (
        f"https://{lang}.wikipedia.org/w/api.php"
        "?action=query&prop=pageimages&format=json"
        f"&titles={requests.utils.quote(title)}&pithumbsize=500"
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

def fetch_wiki_image(name: str) -> str | None:
    # 1. Essai Wikipedia EN
    img = _wiki_img("en", WIKI_EN.get(name, name))
    if img:
        return img
    # 2. Fallback Wikipedia FR
    img = _wiki_img("fr", WIKI_FR.get(name, name))
    return img

communes_raw = [
    # ── Île-de-France ──────────────────────────────────────────────────────
    {"n":"Paris","de":"Paris (75)","rg":"Île-de-France","po":2161000,"ar":105,"fa":"Capital and most visited city in the world (30M tourists/year); home to the Eiffel Tower, the Louvre and Notre-Dame; built on a Seine island first settled by the Parisii tribe around 250 BC"},
    {"n":"Versailles","de":"Yvelines (78)","rg":"Île-de-France","po":88000,"ar":26,"fa":"The Palace of Versailles (1661-1710) became the symbol of royal absolutism; the Hall of Mirrors witnessed the proclamation of the German Empire (1871) and the signing of the Treaty of Versailles (1919)"},
    {"n":"Fontainebleau","de":"Seine-et-Marne (77)","rg":"Île-de-France","po":15000,"ar":172,"fa":"Napoleon's preferred royal residence — he signed his first abdication here in 1814; the 17,000-hectare UNESCO forest was the birthplace of the Barbizon landscape painting school"},
    {"n":"Saint-Germain-en-Laye","de":"Yvelines (78)","rg":"Île-de-France","po":43000,"ar":49,"fa":"Birthplace of Louis XIV (1638) and Claude Debussy (1862); the Treaty of Saint-Germain-en-Laye (1919) dismantled the Austro-Hungarian Empire; the National Archaeology Museum is housed in its royal château"},
    {"n":"Meaux","de":"Seine-et-Marne (77)","rg":"Île-de-France","po":57000,"ar":20,"fa":"Famous for Brie de Meaux — AOC-protected since 1980 and described as the 'king of cheeses'; a cathedral started in 1050; Bishop Bossuet preached here and delivered the greatest funeral orations in French literature"},
    {"n":"Provins","de":"Seine-et-Marne (77)","rg":"Île-de-France","po":12000,"ar":43,"fa":"UNESCO-listed medieval market town; one of the six Champagne trade fair cities in the Middle Ages; its roses were adopted as heraldic symbols by English royalty during the Wars of the Roses"},
    {"n":"Melun","de":"Seine-et-Marne (77)","rg":"Île-de-France","po":42000,"ar":16,"fa":"Capital of Seine-et-Marne; Brie de Melun is older than Brie de Meaux — monks produced it in the 7th century; its medieval bridge and Notre-Dame Cathedral predate Notre-Dame de Paris; Philippe Auguste was crowned king here"},
    {"n":"Rambouillet","de":"Yvelines (78)","rg":"Île-de-France","po":26000,"ar":113,"fa":"The French presidential retreat since 1897; Marie Antoinette had a model farm here; the Treaty of Rambouillet (1999) was the failed final diplomatic attempt to prevent the Kosovo War"},
    {"n":"Nanterre","de":"Hauts-de-Seine (92)","rg":"Île-de-France","po":95000,"ar":12,"fa":"La Défense — France's Manhattan — borders Nanterre with 69 skyscrapers housing 180,000 workers; the May 1968 student revolt began at Nanterre University; the Grande Arche aligns precisely with the Louvre and Arc de Triomphe"},
    # ── Hauts-de-France ──────────────────────────────────────────────────────
    {"n":"Lille","de":"Nord (59)","rg":"Hauts-de-France","po":232000,"ar":35,"fa":"Flemish capital of France; la Braderie de Lille is the world's largest flea market (first September weekend, 600,000 visitors); birthplace of Charles de Gaulle; the Vieille Bourse (1653) is France's finest Flemish Baroque monument"},
    {"n":"Amiens","de":"Somme (80)","rg":"Hauts-de-France","po":133000,"ar":50,"fa":"Its Gothic cathedral has the tallest nave in France (42.5m); Jules Verne lived and is buried here; medieval floating market gardens (hortillonnages) operate on 65km of canals"},
    {"n":"Arras","de":"Pas-de-Calais (62)","rg":"Hauts-de-France","po":43000,"ar":30,"fa":"Two baroque Grand Places form one of northern Europe's finest urban ensembles; birthplace of Robespierre; Wellington's tunnels sheltered 24,000 Allied troops before the 1917 Arras offensive"},
    {"n":"Calais","de":"Pas-de-Calais (62)","rg":"Hauts-de-France","po":73000,"ar":26,"fa":"Busiest passenger port in the world (21M crossings/year); held by England for 211 years (1347-1558) — the last English territory in France; Rodin's Burghers of Calais (1889) is a masterpiece of Western sculpture"},
    {"n":"Dunkerque","de":"Nord (59)","rg":"Hauts-de-France","po":88000,"ar":44,"fa":"Operation Dynamo (May-June 1940) evacuated 338,000 Allied soldiers from its beaches in 9 days; hosts Europe's most spectacular carnival (80,000 costumed revellers); France's third largest port after Marseille and Le Havre"},
    {"n":"Valenciennes","de":"Nord (59)","rg":"Hauts-de-France","po":44000,"ar":22,"fa":"Birthplace of painters Watteau (1684) and Carpeaux (1827); Valenciennes lace was the finest in Europe in the 17th century, worn by Marie Antoinette; former coal and steel city transformed into a cultural hub"},
    {"n":"Laon","de":"Aisne (02)","rg":"Hauts-de-France","po":25000,"ar":33,"fa":"Its extraordinary Gothic cathedral (1155-1235) stands atop a rocky plateau 100m above the Laon plain; one of the first great Gothic cathedrals, directly influencing Notre-Dame de Paris; five medieval towers still crown the hilltop city"},
    {"n":"Senlis","de":"Oise (60)","rg":"Hauts-de-France","po":16500,"ar":18,"fa":"One of France's oldest cities (Roman Augustomagus); its Gothic cathedral (1153) directly influenced Notre-Dame de Paris; Merovingian and Carolingian kings hunted in the surrounding royal forest"},
    {"n":"Compiègne","de":"Oise (60)","rg":"Hauts-de-France","po":40000,"ar":21,"fa":"WWI Armistice signed in a railway carriage in the forest here (November 11, 1918); Hitler used the same carriage for France's 1940 armistice before ordering it destroyed; Joan of Arc was captured near here (1430)"},
    {"n":"Beauvais","de":"Oise (60)","rg":"Hauts-de-France","po":55000,"ar":22,"fa":"Its Gothic cathedral was begun in 1225 with the highest choir vault ever built (48.5m) — it partially collapsed in 1284; only the choir was completed, making it the greatest unfinished Gothic cathedral in history"},
    {"n":"Chantilly","de":"Oise (60)","rg":"Hauts-de-France","po":12000,"ar":17,"fa":"The Château de Chantilly holds the second-finest art collection in France after the Louvre; home to the world's most prestigious flat races (Prix du Jockey Club); whipped Chantilly cream was invented by François Vatel here in 1671"},
    # ── Normandie ────────────────────────────────────────────────────────────
    {"n":"Rouen","de":"Seine-Maritime (76)","rg":"Normandie","po":112000,"ar":21,"fa":"Joan of Arc was burned at the stake here in 1431; Monet painted its Gothic cathedral 30 times in different lights; Richard the Lionheart's heart is buried in the cathedral; Flaubert set Madame Bovary in this region"},
    {"n":"Caen","de":"Calvados (14)","rg":"Normandie","po":107000,"ar":26,"fa":"William the Conqueror's capital; the Mémorial de Caen is France's finest WWII museum; 75% of the city was destroyed in the 1944 Battle of Normandy and masterfully rebuilt from scratch within a decade"},
    {"n":"Le Havre","de":"Seine-Maritime (76)","rg":"Normandie","po":171000,"ar":47,"fa":"UNESCO-listed modernist city: Auguste Perret rebuilt it entirely in reinforced concrete after WWII bombing; France's second largest port; Monet spent his youth here and painted his first impressionist harbour views"},
    {"n":"Bayeux","de":"Calvados (14)","rg":"Normandie","po":14000,"ar":12,"fa":"The Bayeux Tapestry (70m, 1070) depicts the Norman Conquest of England in comic-strip form; first French city liberated (June 7, 1944) — Charles de Gaulle made his famous speech from its balcony"},
    {"n":"Giverny","de":"Eure (27)","rg":"Normandie","po":500,"ar":5,"fa":"Claude Monet lived here from 1883 until his death in 1926; his water lily garden directly inspired 250 paintings; 500,000 visitors come each year to see the pink house, Japanese bridge and flower gardens"},
    {"n":"Mont-Saint-Michel","de":"Manche (50)","rg":"Normandie","po":30,"ar":1,"fa":"Tidal island topped by an 8th-century abbey; France's most visited monument outside Paris (3.5M visitors/year); the bay has Europe's highest tidal range (up to 15m); 'the marvel of the Western world'"},
    {"n":"Cherbourg-en-Cotentin","de":"Manche (50)","rg":"Normandie","po":80000,"ar":84,"fa":"The world's largest artificial harbour (completed 1858); the Titanic's last port of call (April 1912); Les Parapluies de Cherbourg (1964) by Jacques Demy was filmed here; gateway to the D-Day beaches"},
    {"n":"Honfleur","de":"Calvados (14)","rg":"Normandie","po":7700,"ar":21,"fa":"Its picturesque Vieux-Bassin harbour inspired the Impressionist movement; Eugène Boudin who taught Monet was born here; Erik Satie was born in a music shop on the Grande Rue (1866); the wooden Sainte-Catherine church is the largest in France"},
    {"n":"Étretat","de":"Seine-Maritime (76)","rg":"Normandie","po":1400,"ar":10,"fa":"The Arch and Needle rock formations are France's most photographed natural monuments; Monet painted them over 80 times; Maurice Leblanc set his Arsène Lupin detective novels here; Guy de Maupassant spent summers nearby"},
    {"n":"Alençon","de":"Orne (61)","rg":"Normandie","po":26000,"ar":21,"fa":"Capital of the world's finest needle lace (point d'Alençon, UNESCO-listed); 17th-century lacemakers went blind working in candlelight on a stitch taking 7 hours per square centimetre; birthplace of Saint Thérèse of Lisieux (1873)"},
    # ── Grand Est ────────────────────────────────────────────────────────────
    {"n":"Strasbourg","de":"Bas-Rhin (67)","rg":"Grand Est","po":285000,"ar":78,"fa":"Capital of European institutions — the European Parliament and Council of Europe; Petite France half-timbered district is UNESCO-listed; changed hands between France and Germany four times since 1870"},
    {"n":"Reims","de":"Marne (51)","rg":"Grand Est","po":182000,"ar":47,"fa":"All but three French kings were crowned in its Gothic cathedral; Champagne country capital — Moët, Veuve Clicquot and Taittinger cellars lie beneath; Germany signed its WWII surrender here (May 7, 1945)"},
    {"n":"Nancy","de":"Meurthe-et-Moselle (54)","rg":"Grand Est","po":104000,"ar":15,"fa":"Place Stanislas — UNESCO-listed, one of Europe's finest baroque squares; birthplace of the École de Nancy Art Nouveau movement and of Victor Hugo (1802)"},
    {"n":"Colmar","de":"Haut-Rhin (68)","rg":"Grand Est","po":68000,"ar":67,"fa":"Most perfectly preserved Alsatian city; its pastel Petite Venise district inspired Hayao Miyazaki; the Isenheim Altarpiece (1515) by Grünewald is one of the greatest German paintings"},
    {"n":"Metz","de":"Moselle (57)","rg":"Grand Est","po":118000,"ar":42,"fa":"Saint-Étienne Cathedral has the world's largest stained glass surface (6,496 m²); a German city 1871-1918 leaving extraordinary Imperial architecture; Centre Pompidou-Metz opened in 2010"},
    {"n":"Troyes","de":"Aube (10)","rg":"Grand Est","po":60000,"ar":13,"fa":"Half-timbered medieval city shaped like a champagne cork; birthplace of Chrétien de Troyes who invented Arthurian romance; the troy ounce for precious metals was standardised at its medieval trade fairs"},
    {"n":"Épernay","de":"Marne (51)","rg":"Grand Est","po":23000,"ar":30,"fa":"Capital of Champagne; Moët & Chandon's 28km of cellars hold 100 million bottles; Dom Pérignon perfected méthode champenoise 20km away; the Avenue de Champagne stores more bottles than there are people in the city"},
    {"n":"Kaysersberg","de":"Haut-Rhin (68)","rg":"Grand Est","po":2800,"ar":17,"fa":"Birthplace of Albert Schweitzer (Nobel Peace Prize, 1952); one of Alsace's most perfectly preserved medieval villages; its fortified bridge over the Weiss is unique in France"},
    {"n":"Verdun","de":"Meuse (55)","rg":"Grand Est","po":18000,"ar":38,"fa":"The Battle of Verdun (1916) — 300 days, 700,000 casualties — became the defining symbol of WWI's industrial-scale slaughter; the Douaumont Ossuary contains the bones of 130,000 unidentified soldiers"},
    {"n":"Obernai","de":"Bas-Rhin (67)","rg":"Grand Est","po":11500,"ar":17,"fa":"One of Alsace's most photogenic towns with intact medieval ramparts, towers and market square; a major hop-growing town supplying Alsatian breweries; the Kochersberg produces the hops for Kronenbourg"},
    {"n":"Riquewihr","de":"Haut-Rhin (68)","rg":"Grand Est","po":1300,"ar":4,"fa":"Completely preserved medieval Alsatian wine village; the Dolder tower (1291) is the finest example of Alsatian military architecture; its Rieslings have been exported since the 16th century and are considered among the world's finest"},
    {"n":"Épinal","de":"Vosges (88)","rg":"Grand Est","po":32000,"ar":63,"fa":"The Imagerie d'Épinal — colourful popular prints — gave French the phrase 'image d'Épinal' for an idealised simplified view; mass-produced since 1796; the Musée de l'Image holds over 100,000 prints"},
    {"n":"Domrémy-la-Pucelle","de":"Vosges (88)","rg":"Grand Est","po":130,"ar":10,"fa":"Birthplace of Joan of Arc (January 6, 1412); the farmhouse where she grew up still stands; she heard her first voices of Saints Michael, Catherine and Margaret in the nearby garden at age 13"},
    {"n":"Rocroi","de":"Ardennes (08)","rg":"Grand Est","po":2200,"ar":37,"fa":"France's finest intact Vauban star fortress; the Battle of Rocroi (1643) — where 22-year-old Condé defeated the Spanish tercios — marked the end of Spanish military supremacy in Europe; fully preserved ramparts encircle the tiny town"},
    {"n":"Belfort","de":"Territoire de Belfort (90)","rg":"Bourgogne-Franche-Comté","po":47000,"ar":16,"fa":"The Lion of Belfort — a 22m lion carved by Bartholdi (sculptor of the Statue of Liberty) — commemorates the 103-day resistance against 40,000 Prussians (1870-71); the gap it guards is called the Trouée de Belfort"},
    # ── Bretagne ─────────────────────────────────────────────────────────────
    {"n":"Rennes","de":"Ille-et-Vilaine (35)","rg":"Bretagne","po":217000,"ar":50,"fa":"Capital of Brittany; the Parliament of Brittany (1654) survived the great fire of 1720; one of France's liveliest student cities; the Breton parliament resisted royal authority for centuries"},
    {"n":"Brest","de":"Finistère (29)","rg":"Bretagne","po":142000,"ar":49,"fa":"France's main Atlantic naval base since Richelieu; at the westernmost tip of continental France; almost entirely rebuilt after WWII bombing; home to the Oceanopolis aquarium (60,000 marine animals)"},
    {"n":"Saint-Malo","de":"Ille-et-Vilaine (35)","rg":"Bretagne","po":44000,"ar":157,"fa":"Corsair city — privateers raided British shipping under royal licence; birthplace of Jacques Cartier who claimed Canada (1534) and Chateaubriand; the walled city juts into the sea on a granite promontory"},
    {"n":"Carnac","de":"Morbihan (56)","rg":"Bretagne","po":4200,"ar":33,"fa":"World's largest megalithic complex: over 3,000 menhirs in parallel alignments, erected 3300-4500 BC; their purpose (astronomical? ritual?) remains one of the great mysteries of prehistoric archaeology"},
    {"n":"Quimper","de":"Finistère (29)","rg":"Bretagne","po":62000,"ar":53,"fa":"Heart of Breton Gaelic culture; its twin-spired Gothic Cathedral dates from 1239; Quimper faience pottery has been produced since 1690 with distinctive Celtic folk motifs; hosts the Festival de Cornouaille"},
    {"n":"Vannes","de":"Morbihan (56)","rg":"Bretagne","po":56000,"ar":32,"fa":"Completely preserved medieval ramparts and towers; Brittany was formally annexed to France by treaty here in 1532; the Morbihan Gulf — an inland sea with 40 islands — lies at the city's doorstep"},
    {"n":"Dinan","de":"Côtes-d'Armor (22)","rg":"Bretagne","po":11000,"ar":23,"fa":"One of Brittany's best-preserved medieval towns with 3km of 14th-century walls; the Breton hero Bertrand du Guesclin — who liberated France from English occupation — is honoured with his own museum here"},
    {"n":"Pont-Aven","de":"Finistère (29)","rg":"Bretagne","po":2700,"ar":18,"fa":"Paul Gauguin and his school of Post-Impressionism was born here in 1886; 'I love Brittany — there I find the wild and the primitive' wrote Gauguin; today 60 art galleries occupy this village of 2,700"},
    {"n":"Concarneau","de":"Finistère (29)","rg":"Bretagne","po":19000,"ar":47,"fa":"One of France's largest fishing ports; its Ville Close (walled town) sits on an island in the bay connected by a drawbridge; home of the first French canning factories; hosts the Fête des Filets Bleus since 1905"},
    {"n":"Quiberon","de":"Morbihan (56)","rg":"Bretagne","po":5100,"ar":8,"fa":"Peninsula connected to the mainland by a narrow strip of land; in 1795, émigré Royalists landed here but were captured and executed in the 'Quiberon expedition'; gateway to Belle-Île-en-Mer; sardine fishing tradition"},
    # ── Pays de la Loire ─────────────────────────────────────────────────────
    {"n":"Nantes","de":"Loire-Atlantique (44)","rg":"Pays de la Loire","po":320000,"ar":65,"fa":"Birthplace of Jules Verne; the Machines de l'Île mechanical elephant processes through crowds; the Edict of Nantes (1598) granted religious freedom to Protestants; the Dukes of Brittany castle dominates the city"},
    {"n":"Le Mans","de":"Sarthe (72)","rg":"Pays de la Loire","po":147000,"ar":52,"fa":"The 24 Hours of Le Mans — world's oldest motor endurance race (since 1923); Richard I of England (the Lionheart) was born in its Plantagenet city (1157); its Romanesque Cathedral nave has exceptional 12th-century frescoes"},
    {"n":"Angers","de":"Maine-et-Loire (49)","rg":"Pays de la Loire","po":151000,"ar":43,"fa":"The Château d'Angers houses the Apocalypse Tapestry (1375-1382) — 140m long, the world's oldest and largest medieval tapestry; the Anjou produces France's finest Chenin Blanc wines"},
    {"n":"Saint-Nazaire","de":"Loire-Atlantique (44)","rg":"Pays de la Loire","po":69000,"ar":72,"fa":"Shipyards built the SS Normandie (1935) and Queen Mary 2 (2004); the WWII German submarine base — most massive Nazi structure in France (480,000 m³ concrete) — is now a cultural centre and concert venue"},
    {"n":"Guérande","de":"Loire-Atlantique (44)","rg":"Pays de la Loire","po":16000,"ar":68,"fa":"Perfectly preserved medieval walled town; the Guérande salt marshes produce the world's finest fleur de sel, hand-harvested from 350-year-old salt pans by the Paludiers guild; the pans have been certified organic since 2018"},
    {"n":"Laval","de":"Mayenne (53)","rg":"Pays de la Loire","po":50000,"ar":36,"fa":"Birthplace of Henri Rousseau (1844) — the naïve painter who depicted jungles he never visited while working as a customs officer; Alfred Jarry, inventor of 'pataphysics' and absurdist theatre, was also born here"},
    # ── Centre-Val de Loire ──────────────────────────────────────────────────
    {"n":"Orléans","de":"Loiret (45)","rg":"Centre-Val de Loire","po":114000,"ar":28,"fa":"Joan of Arc lifted the English siege here in May 1429, turning the Hundred Years War; the Fête de Jeanne d'Arc (May 7-8) has been celebrated since 1430 — the oldest annual commemoration in French history"},
    {"n":"Chartres","de":"Eure-et-Loir (28)","rg":"Centre-Val de Loire","po":39000,"ar":16,"fa":"Its Gothic cathedral (1194) is the summit of Gothic art; medieval stained glass (172 windows, 2,700 m²) is the finest preserved anywhere; visible from 30km across the Beauce plain; the labyrinth guides symbolic pilgrims"},
    {"n":"Tours","de":"Indre-et-Loire (37)","rg":"Centre-Val de Loire","po":135000,"ar":35,"fa":"Heart of the Loire Valley châteaux; French linguists consider the Tourain accent to be the purest French; Leonardo da Vinci spent his last years 25km away; the Battle of Tours (732) halted Islamic expansion nearby"},
    {"n":"Blois","de":"Loir-et-Cher (41)","rg":"Centre-Val de Loire","po":47000,"ar":23,"fa":"Four French kings — Louis XII, François I, Henri III, Henri IV — lived in Blois Royal Castle; the Duke of Guise was assassinated here by Henri III's guards in 1588 in a plot that shocked Europe"},
    {"n":"Amboise","de":"Indre-et-Loire (37)","rg":"Centre-Val de Loire","po":12500,"ar":39,"fa":"Leonardo da Vinci spent his last three years here (1516-1519) at François I's invitation; he is buried in the Chapel of Saint-Hubert; his manor Clos Lucé is now a museum of his machines and inventions"},
    {"n":"Chinon","de":"Indre-et-Loire (37)","rg":"Centre-Val de Loire","po":8500,"ar":38,"fa":"Joan of Arc recognised the disguised Dauphin Charles VII among 300 courtiers here in 1429, launching her mission; birthplace of François Rabelais; the Chinon wine is one of the Loire's finest Cabernet Francs"},
    {"n":"Azay-le-Rideau","de":"Indre-et-Loire (37)","rg":"Centre-Val de Loire","po":3400,"ar":37,"fa":"The château (1518-1527) built on an island in the Indre river is considered the masterpiece of French Renaissance architecture; its reflection in the water inspired dozens of painters; Leonardo reportedly advised on its design"},
    {"n":"Loches","de":"Indre-et-Loire (37)","rg":"Centre-Val de Loire","po":6500,"ar":36,"fa":"France's best-preserved medieval royal keep and dungeon; Richard the Lionheart stormed it in 3 hours in 1194 after it had held for a year; Joan of Arc convinced Charles VII to march to Reims from the castle here"},
    {"n":"Bourges","de":"Cher (18)","rg":"Centre-Val de Loire","po":66000,"ar":68,"fa":"Its Gothic Cathedral Saint-Étienne (1195) is UNESCO-listed with five doorways; the palace of Jacques Cœur (Charles VII's financier) is the finest 15th-century secular building in France"},
    # ── Bourgogne-Franche-Comté ──────────────────────────────────────────────
    {"n":"Dijon","de":"Côte-d'Or (21)","rg":"Bourgogne-Franche-Comté","po":157000,"ar":40,"fa":"Burgundy's capital; the Dukes of Burgundy once ruled a territory rivalling France; world mustard capital since the 14th century; the Route des Grands Crus wine road begins here"},
    {"n":"Beaune","de":"Côte-d'Or (21)","rg":"Bourgogne-Franche-Comté","po":22000,"ar":38,"fa":"Heart of Burgundy wine country; the Hôtel-Dieu (1443) with its polychrome tile roof holds the world's most prestigious charity wine auction each November; founded to earn divine redemption for Chancellor Nicolas Rolin's sins"},
    {"n":"Besançon","de":"Doubs (25)","rg":"Bourgogne-Franche-Comté","po":133000,"ar":65,"fa":"Birthplace of Victor Hugo (1802); Vauban's star-shaped citadel is UNESCO-listed; centre of French precision watchmaking; the Lumière brothers held their first public cinema screening in Besançon (January 1896)"},
    {"n":"Vézelay","de":"Yonne (89)","rg":"Bourgogne-Franche-Comté","po":450,"ar":15,"fa":"Romanesque Basilica of Sainte-Marie-Madeleine (1104) is UNESCO-listed and a major Camino start; the Second Crusade was preached here by St Bernard (1146); Mary Magdalene's relics draw pilgrims still"},
    {"n":"Auxerre","de":"Yonne (89)","rg":"Bourgogne-Franche-Comté","po":35000,"ar":28,"fa":"Its Cathedral Saint-Étienne has the world's finest collection of 12th-century Romanesque stained glass; perched above the Yonne river; gateway to the Chablis wine appellation"},
    {"n":"Cluny","de":"Saône-et-Loire (71)","rg":"Bourgogne-Franche-Comté","po":4400,"ar":22,"fa":"The Abbaye de Cluny (founded 910) was the largest Christian building in the world for 400 years, housing 10,000 monks at its peak; the Cluniac Order reformed European monasticism; only ruins remain after the French Revolution"},
    {"n":"Mâcon","de":"Saône-et-Loire (71)","rg":"Bourgogne-Franche-Comté","po":33000,"ar":26,"fa":"Birthplace of the Romantic poet Alphonse de Lamartine; the Mâconnais produces the finest white Burgundy; the Roche de Solutré — an iconic limestone outcrop — was climbed every Whit Sunday by François Mitterrand for 30 years"},
    {"n":"Nevers","de":"Nièvre (58)","rg":"Bourgogne-Franche-Comté","po":33000,"ar":34,"fa":"The incorruptible body of Saint Bernadette Soubirous lies in a glass coffin in a chapel here; Nevers porcelain has been produced since the 16th century; the Formula 1 French Grand Prix was held at Magny-Cours 12km away"},
    {"n":"Semur-en-Auxois","de":"Côte-d'Or (21)","rg":"Bourgogne-Franche-Comté","po":4100,"ar":45,"fa":"One of Burgundy's best-preserved medieval towns; four pink granite towers overlook the Armançon river in a ravine; the oldest hippodrome in France (1627) hosts the 15,000-person 'Grand Prix de Semur'"},
    # ── Auvergne-Rhône-Alpes ────────────────────────────────────────────────
    {"n":"Lyon","de":"Métropole de Lyon (69)","rg":"Auvergne-Rhône-Alpes","po":522000,"ar":48,"fa":"France's gastronomic capital; the Lumière brothers invented cinema here in 1895; its UNESCO-listed Presqu'île is built between the Rhône and Saône; the Traboules are secret Renaissance passageways through its old town"},
    {"n":"Grenoble","de":"Isère (38)","rg":"Auvergne-Rhône-Alpes","po":158000,"ar":18,"fa":"Hosted the 1968 Winter Olympics; birthplace of Stendhal; surrounded by three mountain massifs; home of Chartreuse liqueur and the ESRF particle physics laboratory"},
    {"n":"Clermont-Ferrand","de":"Puy-de-Dôme (63)","rg":"Auvergne-Rhône-Alpes","po":143000,"ar":42,"fa":"Michelin tire HQ since 1889; its Romanesque cathedral is built entirely from black volcanic volvic stone; Pope Urban II launched the First Crusade from here in 1095"},
    {"n":"Annecy","de":"Haute-Savoie (74)","rg":"Auvergne-Rhône-Alpes","po":125000,"ar":66,"fa":"Venice of the Alps; Lake Annecy has been named Europe's cleanest lake; birthplace of Jean-Jacques Rousseau; the 12th-century canals and the Palais de l'Isle are among France's most photographed sights"},
    {"n":"Chamonix","de":"Haute-Savoie (74)","rg":"Auvergne-Rhône-Alpes","po":8700,"ar":245,"fa":"Gateway to Mont Blanc (4,808m) — Western Europe's highest peak; hosted the inaugural Winter Olympics in 1924; the Aiguille du Midi cable car climbs 2,807m in 20 minutes above the clouds"},
    {"n":"Saint-Étienne","de":"Loire (42)","rg":"Auvergne-Rhône-Alpes","po":175000,"ar":80,"fa":"The first French railway opened here in 1827; former coal and arms manufacturing capital transformed into a UNESCO Creative City of Design; birthplace of the bicycle and the modern military rifle"},
    {"n":"Chambéry","de":"Savoie (73)","rg":"Auvergne-Rhône-Alpes","po":62000,"ar":19,"fa":"Ancient capital of the House of Savoy; the Holy Shroud was kept in its Sainte-Chapelle before moving to Turin in 1578; Jean-Jacques Rousseau lived here with his mentor Madame de Warens"},
    {"n":"Le Puy-en-Velay","de":"Haute-Loire (43)","rg":"Auvergne-Rhône-Alpes","po":18500,"ar":33,"fa":"One of the four main starting points of the Camino de Santiago; a 16m Notre-Dame statue stands atop an 82m volcanic plug; world capital of lace-making (dentelle du Puy, UNESCO heritage)"},
    {"n":"Aurillac","de":"Cantal (15)","rg":"Auvergne-Rhône-Alpes","po":27000,"ar":49,"fa":"Gerbert d'Aurillac born here became Pope Sylvester II (999 AD) — the first French pope — and introduced Arabic numerals, the abacus and the mechanical clock to medieval Europe"},
    {"n":"Moulins","de":"Allier (03)","rg":"Auvergne-Rhône-Alpes","po":18000,"ar":25,"fa":"Capital of the Bourbonnais; the Moulins Triptych (1498) is considered the masterpiece of French Gothic painting; Coco Chanel grew up in its orphanage and launched her career in nearby Vichy"},
    {"n":"Bourg-en-Bresse","de":"Ain (01)","rg":"Auvergne-Rhône-Alpes","po":40000,"ar":29,"fa":"Capital of the world's finest poultry appellation (Bresse chicken, AOC since 1957); the Royal Monastery of Brou (1532) has the most ornate Flamboyant Gothic interior in France"},
    {"n":"Vichy","de":"Allier (03)","rg":"Auvergne-Rhône-Alpes","po":24000,"ar":11,"fa":"The thermal spa capital drawing Napoleon III and European royalty; the Vichy government of Marshal Pétain collaborated with Nazi Germany here (1940-1944) — a defining trauma of French national memory; still bottling its mineral water"},
    {"n":"Privas","de":"Ardèche (07)","rg":"Auvergne-Rhône-Alpes","po":9500,"ar":29,"fa":"Capital of Ardèche; world capital of marrons glacés — crystallised chestnuts produced from the Ardèche chestnut forests since the 17th century; the spectacular Gorges de l'Ardèche (300m deep) cut through limestone 10km away"},
    {"n":"Thiers","de":"Puy-de-Dôme (63)","rg":"Auvergne-Rhône-Alpes","po":11000,"ar":61,"fa":"Cutlery capital of France since the 14th century — 70% of French knives are still made here; the Durolle valley powered hundreds of blade-grinding workshops; the Maison des Couteliers museum tells the 700-year story of the craft"},
    {"n":"Évian-les-Bains","de":"Haute-Savoie (74)","rg":"Auvergne-Rhône-Alpes","po":8500,"ar":18,"fa":"Source of the world's most consumed mineral water (Évian), discovered in 1789 by the Marquis de Lessert; the Évian Masters golf tournament hosts the only women's major in Europe; faces Lausanne across Lake Geneva"},
    # ── Provence-Alpes-Côte d'Azur ──────────────────────────────────────────
    {"n":"Marseille","de":"Bouches-du-Rhône (13)","rg":"Provence-Alpes-Côte d'Azur","po":870000,"ar":241,"fa":"France's oldest city (600 BC, founded as Massalia by Greek settlers) and largest Mediterranean port; birthplace of La Marseillaise national anthem; the MuCEM museum sits at the entrance of the ancient harbour"},
    {"n":"Nice","de":"Alpes-Maritimes (06)","rg":"Provence-Alpes-Côte d'Azur","po":340000,"ar":72,"fa":"Capital of the French Riviera; the Promenade des Anglais was built in 1820 for English tourists; ceded by Italy to France only in 1860; birthplace of Garibaldi; its Niçois cuisine is distinct from the rest of France"},
    {"n":"Toulon","de":"Var (83)","rg":"Provence-Alpes-Côte d'Azur","po":172000,"ar":43,"fa":"France's main naval base since 1707; Napoleon recaptured it from English-Royalist forces at age 24 (1793) — his first major military success; the French fleet was scuttled here in 1942 to prevent German capture"},
    {"n":"Avignon","de":"Vaucluse (84)","rg":"Provence-Alpes-Côte d'Azur","po":93000,"ar":65,"fa":"The Papacy moved here from Rome in 1309 and stayed 70 years; the Palais des Papes is the largest Gothic palace in the world; the Sur le Pont d'Avignon song is known by every French child"},
    {"n":"Aix-en-Provence","de":"Bouches-du-Rhône (13)","rg":"Provence-Alpes-Côte d'Azur","po":143000,"ar":186,"fa":"Birthplace of Paul Cézanne who painted Mont Sainte-Victoire over 60 times; a Roman thermal spa town (Aquae Sextiae, 123 BC) founded after the first great Roman victory in Gaul"},
    {"n":"Arles","de":"Bouches-du-Rhône (13)","rg":"Provence-Alpes-Côte d'Azur","po":52000,"ar":759,"fa":"Largest commune in metropolitan France (759 km²); Van Gogh produced 300 paintings here in 14 months; its Roman amphitheatre (1st century BC) still hosts bullfights; UNESCO World Heritage city"},
    {"n":"Cannes","de":"Alpes-Maritimes (06)","rg":"Provence-Alpes-Côte d'Azur","po":75000,"ar":19,"fa":"The International Film Festival (since 1946) awards the Palme d'Or; a quiet fishing village until Lord Brougham was stranded here in 1834 and built a villa, starting luxury tourism"},
    {"n":"Orange","de":"Vaucluse (84)","rg":"Provence-Alpes-Côte d'Azur","po":29000,"ar":69,"fa":"The best-preserved Roman theatre in the world (1st century BC) still holds concerts for 8,000; Louis XIV called it 'the finest wall in my kingdom'; the city was a Dutch possession (House of Orange-Nassau) from 1530 to 1713"},
    {"n":"Saint-Tropez","de":"Var (83)","rg":"Provence-Alpes-Côte d'Azur","po":4400,"ar":10,"fa":"A tiny fishing village until Brigitte Bardot filmed And God Created Woman here (1956); Signac, Matisse and Bonnard painted here; 100,000 summer visitors descend on 4,400 permanent residents"},
    {"n":"Les Baux-de-Provence","de":"Bouches-du-Rhône (13)","rg":"Provence-Alpes-Côte d'Azur","po":400,"ar":20,"fa":"Medieval village on white bauxite cliffs; the mineral bauxite (aluminium ore) was named after this village in 1821; the Carrières de Lumières projects art onto the quarry walls for a spectacular immersive show"},
    {"n":"Gordes","de":"Vaucluse (84)","rg":"Provence-Alpes-Côte d'Azur","po":2200,"ar":68,"fa":"Consistently voted one of France's most beautiful villages; perched dramatically above the Luberon valley; famous for prehistoric dry-stone bories and the surrounding lavender fields of the Valensole plateau"},
    {"n":"Menton","de":"Alpes-Maritimes (06)","rg":"Provence-Alpes-Côte d'Azur","po":30000,"ar":15,"fa":"France's warmest city, sheltered by the Alps from northern winds; the Lemon Festival (February) builds monumental sculptures from 145 tons of citrus; Jean Cocteau decorated its wedding hall with his own frescoes"},
    {"n":"Gap","de":"Hautes-Alpes (05)","rg":"Provence-Alpes-Côte d'Azur","po":40000,"ar":218,"fa":"Highest city in the Alps at 735m; Napoleon passed through here on his famous return from Elba (March 1815) via the Route Napoléon; gateway to the Écrins National Park, highest peaks in the Alps after Mont Blanc"},
    {"n":"Sisteron","de":"Alpes-de-Haute-Provence (04)","rg":"Provence-Alpes-Côte d'Azur","po":7400,"ar":96,"fa":"Its 12th-century citadel perched on a rock controls the main pass between Provence and the Alps — the 'Gateway to Provence'; Napoleon breakfasted here on the Route de l'Exil; the Bléone valley is spectacular"},
    {"n":"Hyères","de":"Var (83)","rg":"Provence-Alpes-Côte d'Azur","po":57000,"ar":131,"fa":"France's oldest winter resort, visited by Queen Victoria and Robert Louis Stevenson; its medieval old town and botanical gardens attracted the Belle Époque elite; the Giens salt marshes are an ecological reserve"},
    {"n":"La Ciotat","de":"Bouches-du-Rhône (13)","rg":"Provence-Alpes-Côte d'Azur","po":35000,"ar":33,"fa":"The Lumière brothers filmed L'Arrivée d'un train en gare de La Ciotat here in 1896 — the film that supposedly made audiences flee; the Eden Cinema (1889) is the oldest still-operating cinema in the world"},
    {"n":"Briançon","de":"Hautes-Alpes (05)","rg":"Provence-Alpes-Côte d'Azur","po":12000,"ar":174,"fa":"Highest city in France and the EU at 1,326m; Vauban's star-shaped ramparts are UNESCO-listed; guards the Montgenèvre pass — the oldest Alpine pass, crossed by Hannibal, Caesar and Napoleon"},
    {"n":"Grasse","de":"Alpes-Maritimes (06)","rg":"Provence-Alpes-Côte d'Azur","po":52000,"ar":44,"fa":"World perfume capital since the 17th century; Chanel No.5's jasmine and May rose are grown here; birthplace of the painter Fragonard; the perfumers Molinard, Galimard and Fragonard still open their workshops to visitors"},
    {"n":"Moustiers-Sainte-Marie","de":"Alpes-de-Haute-Provence (04)","rg":"Provence-Alpes-Côte d'Azur","po":700,"ar":66,"fa":"One of the most beautiful villages in France perched between two cliffs above a ravine; gateway to the Gorges du Verdon (Europe's Grand Canyon); Moustiers faience pottery has been produced here since the 17th century"},
    {"n":"Digne-les-Bains","de":"Alpes-de-Haute-Provence (04)","rg":"Provence-Alpes-Côte d'Azur","po":17000,"ar":195,"fa":"Spa town in the Haute-Provence Alps; a 19th-century Train des Pignes still runs the scenic 150km mountain route to Nice; lavender capital of Provence; Alexandra David-Néel, who walked into Lhasa, lived here"},
    # ── Occitanie ───────────────────────────────────────────────────────────
    {"n":"Toulouse","de":"Haute-Garonne (31)","rg":"Occitanie","po":479000,"ar":118,"fa":"La Ville Rose (pink brick city); Europe's aerospace capital — Airbus, CNES, ATR headquarters; the Basilica of Saint-Sernin (1080) is the largest Romanesque church still standing in the world"},
    {"n":"Montpellier","de":"Hérault (34)","rg":"Occitanie","po":285000,"ar":57,"fa":"France's fastest-growing major city for 30 years; one of Europe's oldest universities (1289); Nostradamus practised medicine here; more than a third of its population are students"},
    {"n":"Carcassonne","de":"Aude (11)","rg":"Occitanie","po":47000,"ar":65,"fa":"Largest medieval fortified city in Western Europe — 52 towers and 3km of double ramparts; besieged during the Cathar Crusade (1209); Viollet-le-Duc controversially restored it in the 19th century"},
    {"n":"Nîmes","de":"Gard (30)","rg":"Occitanie","po":146000,"ar":162,"fa":"Best-preserved Roman monuments outside Italy: the Maison Carrée (19 BC) and its amphitheatre; denim cloth was originally called serge 'de Nîmes' — later shortened to denim by Levi Strauss"},
    {"n":"Perpignan","de":"Pyrénées-Orientales (66)","rg":"Occitanie","po":120000,"ar":69,"fa":"Gateway between France and Spanish Catalonia; Salvador Dalí declared its railway station 'the centre of the universe'; the Palace of the Kings of Majorca (13th century) still dominates the old city"},
    {"n":"Lourdes","de":"Hautes-Pyrénées (65)","rg":"Occitanie","po":14500,"ar":51,"fa":"World's second most-visited pilgrimage site (6M annual pilgrims); the Virgin Mary reportedly appeared to Bernadette Soubirous 18 times in 1858; the town has more hotels per capita than anywhere else in France"},
    {"n":"Albi","de":"Tarn (81)","rg":"Occitanie","po":50000,"ar":178,"fa":"UNESCO Cité épiscopale; its fortress-cathedral (1282) was built to intimidate Cathar heretics; birthplace of Toulouse-Lautrec — his entire estate became a museum in the bishop's palace"},
    {"n":"Narbonne","de":"Aude (11)","rg":"Occitanie","po":53000,"ar":170,"fa":"The Via Domitia — the first Roman road in Gaul (118 BC) — runs through its market; once the capital of Gallia Narbonensis and a great Mediterranean port; its Cathedral's unfinished nave makes it one of the most striking in France"},
    {"n":"Collioure","de":"Pyrénées-Orientales (66)","rg":"Occitanie","po":3000,"ar":14,"fa":"Matisse and Derain invented Fauvism here in the summer of 1905 — the first modern art movement; Picasso, Dufy and dozens of masters painted here; the castle of the Kings of Majorca watches over the bay"},
    {"n":"Uzès","de":"Gard (30)","rg":"Occitanie","po":8500,"ar":49,"fa":"First duchy of France (created 1565); its Tour Fenestrelle is the only round Romanesque bell tower in France; André Gide spent summers at his family estate here; the Place aux Herbes has been a weekly market since the Middle Ages"},
    {"n":"Millau","de":"Aveyron (12)","rg":"Occitanie","po":22000,"ar":170,"fa":"The Millau Viaduct (2004) designed by Norman Foster is the world's tallest bridge (343m above the Tarn gorge); the Grandes Causses sheep produce the milk for Roquefort cheese in the village 25km away"},
    {"n":"Rocamadour","de":"Lot (46)","rg":"Occitanie","po":600,"ar":52,"fa":"Cliff-hanging pilgrimage village built vertically into the Alzou canyon limestone; the Black Madonna chapel has been venerated since the 12th century; 1.5 million visitors per year come to this village of 600 residents"},
    {"n":"Cahors","de":"Lot (46)","rg":"Occitanie","po":21000,"ar":112,"fa":"The Pont Valentré (1378) with three defensive towers is the finest medieval bridge in France; birthplace of Pope John XXII; the Cahors Malbec wine is one of France's oldest appellations"},
    {"n":"Rodez","de":"Aveyron (12)","rg":"Occitanie","po":24000,"ar":47,"fa":"Pink sandstone Gothic cathedral; birthplace of Pierre Soulages whose ultra-black abstract work revolutionised modern art; the Soulages Museum houses the world's largest collection of his work"},
    {"n":"Foix","de":"Ariège (09)","rg":"Occitanie","po":10000,"ar":22,"fa":"Its three-towered castle perched on a volcanic rock is among the most dramatic in the Pyrenees; the cave of Niaux nearby contains Magdalenian bison paintings (13,000 BC)"},
    {"n":"Tarbes","de":"Hautes-Pyrénées (65)","rg":"Occitanie","po":41000,"ar":27,"fa":"Birthplace of Marshal Ferdinand Foch, Supreme Allied Commander who led the WWI victory; the Haras National stud farm (1806) bred the famous Tarbe Anglo-Arab warhorse"},
    {"n":"Auch","de":"Gers (32)","rg":"Occitanie","po":22000,"ar":101,"fa":"Capital of Gascony and Armagnac brandy country; the real D'Artagnan — the musketeer who inspired Dumas — was born 40km away; the Grand Staircase (370 steps) connects the city's upper and lower levels"},
    {"n":"Saint-Jean-Pied-de-Port","de":"Pyrénées-Atlantiques (64)","rg":"Occitanie","po":1700,"ar":35,"fa":"Principal gathering point for the Camino Francés to Santiago de Compostela (790km away); its cobbled rue de la Citadelle has been trodden by pilgrims since the 11th century; 30,000 pilgrims depart here each year"},
    {"n":"Figeac","de":"Lot (46)","rg":"Occitanie","po":10000,"ar":164,"fa":"Birthplace of Jean-François Champollion (1790) who deciphered Egyptian hieroglyphics using the Rosetta Stone; the Champollion Museum displays an original Rosetta Stone cast; the old town's half-timbered houses date from the 14th century"},
    {"n":"Mende","de":"Lozère (48)","rg":"Occitanie","po":12000,"ar":85,"fa":"Capital of Lozère — France's least populated department; its 15th-century Cathedral has the largest bells in France (cast in 1447); gateway to the Gorges du Tarn and the vast wild Margeride granite plateau"},
    {"n":"Montauban","de":"Tarn-et-Garonne (82)","rg":"Occitanie","po":63000,"ar":79,"fa":"Birthplace of Jean-Auguste-Dominique Ingres (1780); its museum houses the world's finest Ingres collection; the Pont Vieux (1335) is a masterpiece of Gothic engineering; the first Protestant town in France (1561)"},
    {"n":"Moissac","de":"Tarn-et-Garonne (82)","rg":"Occitanie","po":13000,"ar":97,"fa":"The cloister of the Abbaye de Moissac (1100) is considered the world's finest example of Romanesque sculpture; its tympanum of the Last Judgement (1130) influenced Gothic art across France; a major Camino de Santiago stage"},
    # ── Nouvelle-Aquitaine ───────────────────────────────────────────────────
    {"n":"Bordeaux","de":"Gironde (33)","rg":"Nouvelle-Aquitaine","po":257000,"ar":49,"fa":"World wine capital and home to the Cité du Vin museum; its 18th-century UNESCO-listed port city was built on wine trade wealth; birthplace of Montesquieu (1689) and Michel de Montaigne"},
    {"n":"La Rochelle","de":"Charente-Maritime (17)","rg":"Nouvelle-Aquitaine","po":77000,"ar":28,"fa":"Historic Protestant stronghold besieged by Richelieu (1627-1628); three medieval towers guard the old harbour; Champlain sailed from here to found Quebec; France's largest pleasure marina on the Atlantic"},
    {"n":"Biarritz","de":"Pyrénées-Atlantiques (64)","rg":"Nouvelle-Aquitaine","po":25000,"ar":12,"fa":"Napoleon III built his summer palace here for Empress Eugénie (1854); European surfing capital since the 1950s when Peter Viertel surfed here while filming The Sun Also Rises"},
    {"n":"Sarlat-la-Canéda","de":"Dordogne (24)","rg":"Nouvelle-Aquitaine","po":9000,"ar":99,"fa":"Best-preserved medieval and Renaissance town in France; centre of Périgord foie gras, truffle and walnut production; the Lascaux cave paintings (17,000 BC) are 50km away in the Vézère valley"},
    {"n":"Cognac","de":"Charente (16)","rg":"Nouvelle-Aquitaine","po":19000,"ar":83,"fa":"Sole AOC appellation for Cognac brandy; the black fungus Baudoinia compniacensis coats the limestone walls feeding on the 'angel's share' — 3% of each barrel evaporating yearly"},
    {"n":"Périgueux","de":"Dordogne (24)","rg":"Nouvelle-Aquitaine","po":30000,"ar":64,"fa":"Capital of truffle country; its Saint-Front Cathedral (1120) resembles St Mark's Basilica in Venice; the Vézère valley 50km away contains Lascaux and 147 other prehistoric painted caves"},
    {"n":"Bayonne","de":"Pyrénées-Atlantiques (64)","rg":"Nouvelle-Aquitaine","po":51000,"ar":22,"fa":"Gave its name to the bayonet (17th century); Basque cultural capital; Sephardic Jewish refugees brought chocolate-making from the Americas here in the 17th century, making it France's first chocolate city"},
    {"n":"Pau","de":"Pyrénées-Atlantiques (64)","rg":"Nouvelle-Aquitaine","po":78000,"ar":32,"fa":"Birthplace of Henry IV (1553) — the first Bourbon king; its Boulevard des Pyrénées offers 100km of mountain panorama; Wellington chose it for convalescent English officers after the Napoleonic Wars"},
    {"n":"Poitiers","de":"Vienne (86)","rg":"Nouvelle-Aquitaine","po":88000,"ar":43,"fa":"Charles Martel stopped the Muslim advance into Western Europe at the Battle of Poitiers (732); Eleanor of Aquitaine held her famous Courts of Love here; one of France's oldest universities (1431)"},
    {"n":"Angoulême","de":"Charente (16)","rg":"Nouvelle-Aquitaine","po":42000,"ar":22,"fa":"World capital of bande dessinée (comic books); the International Comics Festival attracts 200,000 visitors in January; Marguerite of Angoulême — sister of François I and Renaissance humanist — was born here"},
    {"n":"Limoges","de":"Haute-Vienne (87)","rg":"Nouvelle-Aquitaine","po":131000,"ar":78,"fa":"World capital of porcelain since 1771 when kaolin clay was discovered nearby; its enamelled metalwork (Limoges enamel) has been exported since the 12th century; Renoir was born here; Les Halles covered market is France's largest"},
    {"n":"Saint-Émilion","de":"Gironde (33)","rg":"Nouvelle-Aquitaine","po":1800,"ar":42,"fa":"UNESCO World Heritage wine village; wines produced here since the 4th century AD (Ausonius had a villa here); the monolithic church carved from a single limestone rock is the largest in the world; Grand Cru classification dates from 1955"},
    {"n":"Saintes","de":"Charente-Maritime (17)","rg":"Nouvelle-Aquitaine","po":26000,"ar":60,"fa":"One of the finest Roman cities in France: the Arc of Germanicus (19 AD) and the Amphitheatre (1st century) are among France's best-preserved Roman monuments; the Saintonge Romanesque style influenced hundreds of churches"},
    {"n":"Niort","de":"Deux-Sèvres (79)","rg":"Nouvelle-Aquitaine","po":60000,"ar":104,"fa":"Capital of the Marais Poitevin — the 'Green Venice' of 180km of navigable channels through a 70,000-hectare marsh; birthplace of Françoise d'Aubigné, later Madame de Maintenon and secret wife of Louis XIV"},
    {"n":"Tulle","de":"Corrèze (19)","rg":"Nouvelle-Aquitaine","po":14000,"ar":75,"fa":"Capital of Corrèze and accordion-making capital of France since 1884; on June 9, 1944 — the day after D-Day — 99 men were hanged from its balconies by the SS Das Reich division in reprisal; Jacques Chirac was MP here for 30 years"},
    {"n":"Bergerac","de":"Dordogne (24)","rg":"Nouvelle-Aquitaine","po":27000,"ar":56,"fa":"The real Cyrano de Bergerac was born in Paris but Edmond Rostand chose this name for his famous play; the town has embraced the fictional Cyrano with statues and a museum; Bergerac wine is one of France's oldest AOC appellations"},
    {"n":"Rochefort","de":"Charente-Maritime (17)","rg":"Nouvelle-Aquitaine","po":24000,"ar":33,"fa":"Built by Colbert in 1666 as an entirely new naval arsenal; the Hermione — the frigate that brought Lafayette to America in 1780 — was reconstructed here over 17 years and sailed to the US in 2015"},
    {"n":"Agen","de":"Lot-et-Garonne (47)","rg":"Nouvelle-Aquitaine","po":32000,"ar":59,"fa":"World capital of prunes (pruneaux d'Agen, AOC); the Agen Bridge (1840) is the longest canal aqueduct in France; the Musée des Beaux-Arts holds Goya's masterpiece Self-Portrait and 14 of his other paintings"},
    # ── Corse ────────────────────────────────────────────────────────────────
    {"n":"Ajaccio","de":"Corse-du-Sud (2A)","rg":"Corse","po":67000,"ar":83,"fa":"Birthplace of Napoleon Bonaparte (August 15, 1769); the Maison Bonaparte is a national museum; Corsica's turquoise waters, maquis scrubland and dramatic mountains define one of the Mediterranean's most unspoilt coastlines"},
    {"n":"Bastia","de":"Haute-Corse (2B)","rg":"Corse","po":44000,"ar":19,"fa":"Largest Corsican city; its Genoese citadel and old port date from the 14th century; Genoa ruled Corsica for 500 years before France purchased it in 1768 — one year before Napoleon's birth"},
    {"n":"Corte","de":"Haute-Corse (2B)","rg":"Corse","po":7000,"ar":267,"fa":"Only inland city of Corsica; historic capital of the independent Corsican Republic (1755-1769) under Pasquale Paoli; home to the only Corsican university; dramatically perched above the Tavignano gorge"},
    # ── DOM & COM ────────────────────────────────────────────────────────────
    {"n":"Fort-de-France","de":"Martinique (972)","rg":"Martinique","po":76000,"ar":44,"fa":"Capital of Martinique; Joséphine de Beauharnais — Napoleon's first wife — was born at Trois-Îlets nearby; the Schoelcher Library (1893) is a Baroque cast-iron building shipped from Paris in pieces for the 1889 World Fair"},
    {"n":"Pointe-à-Pitre","de":"Guadeloupe (971)","rg":"Guadeloupe","po":16000,"ar":3,"fa":"Main commercial city of Guadeloupe, which is shaped like a butterfly; birthplace of Nobel laureate Saint-John Perse (1887); the city has been destroyed and rebuilt multiple times by earthquakes and hurricanes"},
    {"n":"Cayenne","de":"Guyane (973)","rg":"Guyane","po":61000,"ar":24,"fa":"Capital of French Guiana — the only EU territory on mainland South America; the Guiana Space Centre in Kourou (50km away) launches Ariane and Vega rockets; Cayenne pepper was first exported to Europe from here"},
    {"n":"Saint-Denis","de":"La Réunion (974)","rg":"La Réunion","po":147000,"ar":143,"fa":"Capital of Réunion island; gateway to Piton de la Fournaise — one of the world's most active volcanoes (erupts almost annually); the island's Creole culture blends African, Indian, Chinese and French traditions"},
    {"n":"Saint-Pierre","de":"Martinique (972)","rg":"Martinique","po":4400,"ar":43,"fa":"Called the 'Paris of the Caribbean' until 1902; the eruption of Mount Pelée on May 8, 1902 killed all 30,000 inhabitants in minutes — the deadliest volcanic disaster of the 20th century; its ruins are still visible"},
]

def main():
    results = []
    for i, c in enumerate(communes_raw):
        name = c["n"]
        sys.stdout.buffer.write(f"  [{i+1}/{len(communes_raw)}] {name}... ".encode("utf-8"))
        sys.stdout.buffer.flush()
        img = fetch_wiki_image(name)
        entry = dict(c)
        entry["im"] = img
        results.append(entry)
        sys.stdout.buffer.write(("ok\n" if img else "no image\n").encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    with_img = sum(1 for r in results if r["im"])
    out = pathlib.Path("assets/world/communes.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    msg = f"\n{len(results)} communes generees. Images: {with_img}/{len(results)} -> {out}\n"
    sys.stdout.buffer.write(msg.encode("utf-8"))

if __name__ == "__main__":
    main()
