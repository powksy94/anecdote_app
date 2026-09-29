# Chantier "nouvelles catégories" — doc de préparation

Document de travail pour cadrer 7 nouveaux hubs autonomes + 1 restructuration d'un hub existant, avant tout code. Rien n'est codé tant que ce doc n'est pas validé section par section.

Voir aussi [docs/navigation-v3/TECH_PLAN.md](../navigation-v3/TECH_PLAN.md) — la refonte de la navigation (Accueil/Explorer/Recherche/Favoris) rendue nécessaire par l'explosion du nombre de hubs prévue ici.

## Statut

- [ ] Inventions & Tech (nouveau hub)
- [ ] Littérature (nouveau hub)
- [ ] Sport (nouveau hub)
- [ ] Langues & Mots (nouveau hub)
- [ ] Cultures du monde (nouveau hub)
- [ ] Mode (nouveau hub)
- [ ] Mathématiques (nouveau hub)
- [ ] Restructuration du hub Histoire (Événements / Civilisations)

---

## Conventions du projet (rappel)

Chaque catégorie de contenu suit le même pattern dans le code, à reproduire pour toute nouvelle entrée :

- Un enum `ContentType` ([content_type.dart](../../lib/core/models/content_type.dart)) avec, pour chaque nouvelle valeur, une entrée dans 7 fichiers `part` : labels (3 langues via ARB), icône, couleur, dégradé, couleur d'accent, source API/data, drapeaux (`isX`).
- **Le contenu est rédigé à la main**, pas scrapé — voir [generate_famous_artists.py](../../tools/art/generate_famous_artists.py) : chaque entrée a un fait/anecdote écrit spécifiquement pour l'app (ton witty, une accroche factuelle précise, pas un résumé encyclopédique plat). Seule l'**image** est allée chercher automatiquement via l'API Wikipedia (pageimages / REST summary), à partir d'un mapping nom → titre d'article Wikipedia.
- Volume habituel : 50 à 100 entrées par catégorie (voir les scripts existants dans `tools/`).
- Un hub à 2 sous-catégories utilise `HubSplitDialog` (voir [world_navigator.dart](../../lib/features/world/pages/world_navigator.dart)) : un choix gauche/droite, chacun menant à un `SubHubPage` listant ses propres catégories.
- Traduction : les 3 fichiers ARB ([app_en.arb](../../lib/l10n/app_en.arb), [app_fr.arb](../../lib/l10n/app_fr.arb), [app_es.arb](../../lib/l10n/app_es.arb)) doivent rester alignés clé pour clé. Le contenu factuel lui-même est écrit en anglais puis traduit à la volée via Google Translate ([translation_service.dart](../../lib/core/services/translation_service.dart)) — donc pas besoin de rédiger les faits en 3 langues à la main, seulement les libellés d'UI (titres de catégories, etc.) vont dans les ARB.
- Piège connu : toujours vérifier le contraste de la couleur d'accent sur les dégradés sombres/peu saturés (voir mémoire `project_accent_color_contrast`).
- **⚠️ Piège vécu sur Records sportifs (2026-09-29) : le contenu DOIT être rédigé en anglais, jamais en français.** Toute donnée renvoyée par un `Service.getDailyContent()` est traitée par [content_loader.dart](../../lib/core/pages/content_loader.dart) comme la source anglaise (mise en cache sous `locale: 'en'`), puis retraduite à la volée vers FR/ES si besoin. Rédiger directement en français fait donc repasser du français dans Google Translate FR→FR, qui le charcute (ex: "cricket test" transformé en "Test cricket..." en tête de titre). Les 91 entrées de `sport_records.json` ont dû être intégralement retraduites vers l'anglais après ce bug détecté en test réel sur téléphone.

**Nouvelles conventions d'écriture pour les catégories de ce chantier** (décidées en rédigeant les premiers exemples — ne s'appliquent pas rétroactivement aux catégories déjà existantes) :
- **Pas de tiret moyen/long (—) comme séparateur dans le texte du fait**, contrairement au style utilisé dans certaines catégories existantes (ex. `generate_famous_artists.py`). Préférer des phrases complètes, la virgule ou le point-virgule.
- **Pour toute catégorie de personnes, la nationalité doit être accompagnée du vrai drapeau du pays**, pas d'un emoji 🌍 générique. Ça veut dire ajouter un champ code pays ISO2 par personne (comme `country_service.dart` le fait pour les pays : `c.iso2` → emoji drapeau calculé via les indicateurs régionaux Unicode) plutôt qu'une simple chaîne de nationalité libre (comme le fait aujourd'hui `famous_artist_service.dart` avec son `🌍 Nationality: ${a.nationality}` non accompagné d'un vrai drapeau).

---

## 1. Inventions & Tech (nouveau hub)

**Statut : structure proposée — Inventions + Inventeurs, 3 sous-catégories de chaque côté** (comme Art : 3 œuvres + 4 artistes).

**Côté "Inventions" (l'objet/l'idée)**
1. *Grandes inventions* — imprimerie, ampoule, pénicilline, télégraphe, WWW... les classiques qui ont changé le monde
2. *Inventions accidentelles* — post-it, micro-ondes, velcro, champagne... découvertes par erreur
3. *Objets du quotidien* — origine insolite d'objets banals (fermeture éclair, trombone, code-barres, brosse à dents...)

*(Exclu volontairement : informatique/internet pur, pour éviter le chevauchement avec le hub Gaming existant.)*

**Côté "Inventeurs" (la personne)**
1. *Inventeurs légendaires* — Edison, Tesla, Gutenberg, Bell...
2. *Inventeurs méconnus* — angle « vous utilisez leur invention tous les jours sans connaître leur nom » (GPS civil, wifi...) — fort potentiel de surprise
3. *Femmes inventrices* — Hedy Lamarr, Ada Lovelace, Grace Hopper... écho avec `pioneerWoman` déjà dans Célébrités

Exemple de ton visé (à valider) :
> Ampoule électrique — Edison a déposé plus de 1000 brevets dans sa vie, mais la première ampoule à incandescence viable vient en réalité de Joseph Swan, en Angleterre, un an avant lui — les deux ont fini par fusionner leurs entreprises pour éviter un procès.

---

## 2. Littérature (nouveau hub)

**Statut : structure proposée — Œuvres + Écrivains, 3 sous-catégories de chaque côté**, sur le modèle du hub Art (`artWorksHub` / `artArtistsHub`).

**Côté "Œuvres littéraires"**
1. *Romans cultes* — contexte d'écriture, réception scandaleuse ou culte (ex : *Ulysses* interdit aux États-Unis, *1984*, *Lolita*...)
2. *Poésie & théâtre* — poèmes/pièces marquants et leur anecdote de création (Shakespeare, Baudelaire...)
3. *Publications insolites* — manuscrits refusés devenus best-sellers, pseudonymes, scandales éditoriaux (Harry Potter refusé 12 fois, hétéronymes de Pessoa...) — fort potentiel « fun fact »

**Côté "Écrivains"**
1. *Écrivains légendaires* — biographie courte + fait marquant (Hemingway, Woolf, Dostoïevski...)
2. *Écrivains méconnus / redécouverts* — auteurs oubliés puis réhabilités, ou culte underground
3. *Femmes de lettres* — sous-représentées historiquement, cohérence transversale avec « Femmes inventrices » (Tech) et `pioneerWoman` (Célébrités)

Ouvert : couverture géographique/temporelle (occidentale classique uniquement, ou inclut littératures non-occidentales / contemporaines dès le départ ?).

---

## 3. Sport (nouveau hub)

**Statut : structure proposée — Exploits + Athlètes, 3 sous-catégories de chaque côté.**

**Côté "Exploits" (aspect factuel/événementiel, anciennement nommé "Univers")**
1. ✅ *Records sportifs* — 91 entrées rédigées et vérifiées, voir [sport-records-draft.py](sport-records-draft.py) et [tools/sport/generate_sport_records.py](../../tools/sport/generate_sport_records.py). Diversité de sports (~40) et de pays travaillée (Asie du Sud/Est notamment). `ContentType.sportRecord` codé (data/service/dispatcher/labels/icônes/couleurs/dégradé/ARB), en attente de la navigation du hub Sport pour être accessible dans l'app.
2. *Événements légendaires* — matchs/JO mythiques, exploits uniques
3. *Origines & règles insolites* — comment un sport est né, anciennes règles bizarres

**Côté "Athlètes" (la personne)**
1. ✅ *Athlètes légendaires* — récupère `legendaryAthlete`, déjà existant en sous-catégorie Célébrités (59 entrées déjà rédigées, aucune nouvelle rédaction nécessaire). Fait le 2026-09-28 : enrichissement des 59 entrées avec un vrai code pays ISO2 (`cc`) pour afficher le vrai drapeau au lieu d'un 🌍 générique (nouvel utilitaire partagé [flag_emoji.dart](../../lib/core/utils/flag_emoji.dart), réutilisable pour toutes les futures catégories de personnes du chantier). Fait le 2026-09-29 : migration effective vers le hub Sport (`SportNavigator`, retiré de `CelebrityNavigator`), + fix contraste `accentColor` (vert foncé illisible → ambre).
2. ✅ *Rivalités historiques* — 40 entrées rédigées et vérifiées, voir [sport-rivalries-draft.py](sport-rivalries-draft.py) et [tools/sport/generate_sport_rivalries.py](../../tools/sport/generate_sport_rivalries.py). Grands duels sportifs (Federer-Nadal, Ali-Frazier, Senna-Prost, Lin Dan-Lee Chong Wei...), 23 sports différents, aucun sport surreprésenté (max 4/40). Catégorie texte seul, sans image : `ImageContentCard` ne gère qu'un seul portrait, ne convient pas à un duo, donc `ContentType.sportRivalry` utilise automatiquement le `ContentCard` générique (icône + texte) via `selectContentCard` dès que `imageUrl` est `null`. `ContentType.sportRivalry` codé et testé sur device le 2026-09-29 (dégradé indigo/rouge avec icône flèches de comparaison, accentColor ambre lisible, double drapeau ISO2, traduction FR ok).
3. ✅ *Grandes sportives* (remplace "Pionniers & premières") — 66 entrées rédigées et vérifiées, voir [sport-great-women-draft.py](sport-great-women-draft.py) et [tools/sport/generate_sport_great_women.py](../../tools/sport/generate_sport_great_women.py). Grandes athlètes féminines avec contexte socio-historique de leur époque (obstacles rencontrés, portée au-delà du sport), sur le modèle de `pioneerWoman` existant mais avec un `cc` ISO2 pour le vrai drapeau (au lieu du texte libre `co`) et un champ `sp` (sport) en plus. 26 pays représentés, 57/66 photos trouvées (9 sans photo exploitable sur Wikipedia). `ContentType.sportGreatWoman` codé et testé sur device le 2026-09-29 (image bien cadrée, accentColor lisible, traduction FR ok).

Ouvert : quels sports couvrir en priorité (universalité vs sports de niche).

---

## 4. Langues & Mots (nouveau hub)

**Statut : structure proposée — Mots + Expressions.**

**Côté "Mots"**
1. *Étymologies surprenantes* — origine insolite d'un mot courant (« salaire » vient du sel, « assassin » du haschich...)
2. *Mots intraduisibles* — mots d'autres langues sans équivalent direct (hygge, saudade, tsundoku...)
3. *Faux-amis* — mots qui se ressemblent entre langues mais n'ont rien à voir

**Côté "Expressions"** — une catégorie par langue/culture plutôt qu'un fourre-tout "expressions du monde" (qui traiterait toutes les langues non-françaises comme un bloc générique face au français traité à part — à éviter) :
1. *Expressions françaises*
2. *Expressions anglo-saxonnes*
3. *Expressions espagnoles*
4. *Expressions chinoises*
5. *Expressions russes*
6. *Expressions indiennes*

Liste ouverte — à ajuster (nombre de langues, lesquelles prioriser) selon le volume de matière trouvé par langue.

Format très adapté au "fait du jour" (court, punchy, se prête bien à `anecdote`/`preview`+`details`). Fort potentiel de viralité (mots intraduisibles, faux-amis, origines improbables).

---

## 5. Cultures du monde (nouveau hub, indépendant du hub Monde)

**Statut : structure proposée — Fêtes + Traditions, split thématique (pas géographique : chaque catégorie couvre toutes les cultures à égalité, pas de bloc "France" face à un bloc "reste du monde").**

**Côté "Fêtes"**
1. *Grandes fêtes du monde* — origine de fêtes majeures (Nouvel An chinois, Diwali, Dia de los Muertos, Songkran...)
2. *Fêtes insolites* — fêtes locales atypiques (bataille de tomates, festival du hareng...)
3. *Rites de passage* — rituels marquant une étape de vie (mariage, majorité...) selon les cultures

**Côté "Traditions"**
1. *Traditions culinaires* — plat/coutume alimentaire lié à une date ou un événement
2. *Superstitions du monde* — croyances populaires selon les cultures
3. *Costumes & symboles* — vêtements traditionnels, symboles culturels et leur signification

Ouvert : risque de chevauchement avec `country` (déjà dans Territoires) à surveiller pour ne pas raconter deux fois la même chose sur un pays donné.

---

## 6. Mode (nouveau hub autonome)

**Statut : structure proposée — Créations + Designers, 3 sous-catégories de chaque côté**, même principe que Art/Littérature/Tech plutôt qu'une simple extension du hub Art.

**Côté "Créations"**
1. *Pièces iconiques* — la petite robe noire, le jean 501, les Converse, le trench Burberry...
2. *Collections mythiques* — défilés/collections qui ont marqué l'histoire de la mode
3. *Scandales & polémiques* — vêtements ou défilés controversés

**Côté "Designers"**
1. *Couturiers légendaires* — Chanel, Yves Saint Laurent, Dior, McQueen...
2. *Maisons de mode* — origine et histoire de grandes maisons
3. *Pionniers de la mode* — créateurs qui ont changé les codes (premiers à...)

---

## 7. Royauté hors France → restructuration du hub Histoire en 2 sous-hubs

**Statut : structure proposée — le hub Histoire (actuellement flat : `history`, `battle`, `kingOfFrance`, `americanPresident`) passe en split gauche/droite comme les autres hubs.**

**Côté "Événements"**
1. *Histoire au quotidien* — `history` existant ("day in history")
2. *Batailles* — `battle` existant
3. *Scandales diplomatiques* (nouveau)

**Côté "Civilisations"** (renommé — ne se limite pas aux royautés, inclut aussi les présidents)
1. `kingOfFrance` (existant)
2. `americanPresident` (existant)
3. *Monarchie britannique*
4. *Empire ottoman*
5. *Dynasties chinoises*
6. *Empires d'Asie du Sud* (Inde...)
7. *Empires incas & peuples précolombiens d'Amérique*

Ce chantier est donc plus large que prévu : il touche une catégorie déjà existante (restructuration du hub Histoire), pas seulement un ajout.

---

## 8. Mathématiques (nouveau hub autonome — sort de Science non-vivant)

**Statut : structure proposée — Curiosités mathématiques + Mathématiciens.** Vu la richesse trouvée en creusant (6 catégories au total), ça déborde du simple ajout dans `scienceNonLivingHub` prévu initialement — devient un hub à part entière, même logique que Mode.

**Côté "Curiosités mathématiques"**
1. *Nombres fascinants* — pi, nombre d'or, infini, nombres premiers
2. *Origine de certains nombres* — symbolique/historique derrière des nombres précis (666, 616, 69, 42, 13...)
3. *Impossibilités & bizarreries* — la somme de tous les entiers qui "vaut" -1/12, la division par zéro, paradoxes logiques (Zénon, Russell...)

**Côté "Mathématiciens"**
1. *Grands mathématiciens* — Pythagore, Euler, Gauss, Fibonacci...
2. *Grands prix* — ⚠️ point de vigilance factuel : il n'existe **pas** de prix Nobel de mathématiques (Nobel ne l'a jamais inclus) ; l'équivalent reconnu est la **médaille Fields** et le **prix Abel** — à utiliser à la place pour rester exact
3. *Mathématiciens les plus surprenants* — histoires insolites (Galois mort en duel à 20 ans, Ramanujan autodidacte, Perelman refusant la médaille Fields et le million de dollars du prix Millennium...)

---

## Proposition d'ordre de réalisation (à discuter, pas encore validé)

Classement proposé du plus au moins engageant, à ajuster ensemble — chaque élément pèse maintenant le même poids de travail (hub complet à 6-7 catégories), donc le critère redevient surtout l'attractivité :

1. **Sport** — audience large, facts à fort potentiel de partage (records, rivalités)
2. **Inventions & Tech** — fort effet "wow", pertinent/actuel
3. **Langues & Mots** — très différenciant, format ultra adapté au "fait du jour", jamais traité par un concurrent direct
4. **Restructuration Histoire** (Civilisations) — capitalise sur `kingOfFrance` qui marche déjà, plus gros morceau (7 catégories rien que côté Civilisations) mais du contenu à très fort potentiel (empires, dynasties, scandales)
5. **Mode** — devenu un hub complet, bon potentiel visuel (pièces iconiques, couturiers)
6. **Cultures du monde** — bon potentiel mais proche thématiquement du hub Monde existant
7. **Littérature** — audience plus restreinte, à valider qu'elle ne fait pas doublon d'intérêt avec Art
8. **Mathématiques** — public le plus incertain (risque de perception "scolaire"), mais les angles "bizarreries" et "mathématiciens surprenants" retenus limitent ce risque

---

## Prochaines étapes

Traiter les sections une par une (dans l'ordre ci-dessus ou un autre) : pour chaque catégorie retenue, valider sa structure interne, rédiger ~10 entrées d'exemple pour caler le ton avant de lancer la rédaction complète des 50-100 entrées, puis seulement passer au code (`ContentType` + parts + script `tools/` + widgets navigator/sub-hub).
