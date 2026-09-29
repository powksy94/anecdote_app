# Refonte navigation 3.0 — doc de préparation

Document de travail pour cadrer la refonte de la navigation principale (style Netflix : Accueil curaté / Explorer / Recherche / Favoris), avant tout code. Rien n'est codé tant que ce doc n'est pas validé section par section.

Contexte : née de la discussion sur [docs/new-categories/TECH_PLAN.md](../new-categories/TECH_PLAN.md) — le hub passerait de 12 à ~19-20 hubs, la grille plate actuelle de l'accueil ne scale plus. Sujet distinct (architecture de navigation) mais dépendant du chantier catégories pour les méta-groupements.

## Statut

- [ ] Onglet Accueil (feed curaté)
- [ ] Onglet Explorer (catalogue complet)
- [ ] Onglet Recherche (navigationnelle, hubs/catégories uniquement)
- [ ] Onglet Favoris (existant, inchangé)
- [ ] Définition des méta-catégories thématiques (transversal Accueil + Explorer)

---

## État actuel (rappel)

[main_shell.dart](../../lib/core/navigation/main_shell.dart) : `NavigationBar` à 2 onglets (Général / Favoris), chacun avec son propre `Navigator` dans un `IndexedStack`. L'onglet "Général" pointe vers [home_page.dart](../../lib/core/pages/home_page.dart), une grille 2 colonnes de tous les `ContentType` top-level (12 aujourd'hui).

---

## Nouvelle structure : 4 onglets

### 1. Accueil (feed curaté, remplace la grille plate actuelle)

Empilement vertical de sections ("rows"), chacune scrollable horizontalement — pattern Netflix/Spotify :

1. *Reprendre* — derniers hubs/sous-catégories visités
2. *Vos favoris* — aperçu (3-5 cartes), pas la liste complète (ça reste le rôle de l'onglet Favoris)
3. *Sélection du jour* — un hub mis en avant, en rotation
4. *Nouveautés* — met en avant les hubs récemment ajoutés (bon débouché pour promouvoir chaque nouveau hub du chantier catégories au fur et à mesure qu'il sort)
5. *Rows thématiques* — une row par méta-catégorie (voir section dédiée plus bas), chacune montrant ses hubs

Ouvert :
- *Reprendre* nécessite de tracker les hubs visités récemment (pas de service existant pour ça — simple à créer : liste de `ContentType` en `shared_preferences`, mise à jour à chaque navigation vers un hub)
- *Sélection du jour* : rotation aléatoire, ou choix éditorial fixe par jour de la semaine ?

### 2. Explorer (catalogue complet, remplace le rôle de l'ancienne page Accueil)

Tout le catalogue, organisé par méta-catégorie en sections (pas un mur plat de 20 cartes). Reprend essentiellement l'ancienne `HomePage` (grille de tous les `ContentType` top-level), mais sectionnée.

Ouvert : dépend de la définition des méta-catégories (voir plus bas) — à figer une fois le chantier catégories suffisamment avancé, certains hubs étant encore en cours de définition.

### 3. Recherche (navigationnelle uniquement — décidé)

Recherche simple sur les titres localisés (ARB) des hubs et sous-catégories — pas de recherche en texte intégral dans le contenu des faits (nécessiterait d'indexer tout le contenu déjà rédigé, chantier technique séparé, écarté pour l'instant). Un `contains` insensible à la casse/accents suffit vu le volume (~20 hubs, ~80-100 sous-catégories) — pas besoin d'un moteur de recherche dédié.

Résultats groupés par hub parent quand le match est sur une sous-catégorie (ex. taper "échecs" doit remonter la sous-catégorie et indiquer dans quel hub elle se trouve).

Ouvert : historique de recherches récentes ? suggestions à l'ouverture (avant frappe) ?

### 4. Favoris (inchangé)

Pas de changement de fonctionnement, juste sa place dans la barre passe de 2e à 4e onglet.

---

## Méta-catégories thématiques (transversal Accueil + Explorer)

Pistes de regroupement (à valider une fois tous les nouveaux hubs du chantier catégories définis) :
- **Culture** — Art, Littérature, Mode, Musique, Cinéma
- **Savoir** — Science, Mathématiques, Inventions & Tech
- **Monde** — Monde (géographie), Cultures du monde, Histoire
- **Divertissement** — Gaming, Sport
- **Vie & société** — Santé, Langues & Mots, Célébrités, Mythologie

Ouvert : certains hubs sont ambigus (Célébrités pourrait aller dans plusieurs groupes ; Mythologie pourrait rejoindre Histoire ou Culture) — à trancher plus tard, pas bloquant pour le reste de ce doc.

---

## Impact technique (aperçu, pas encore détaillé)

- `MainShell` passe de 2 à 4 entrées dans l'`IndexedStack`/`NavigationBar`
- L'actuelle `HomePage` (grille plate) devient la base de la page **Explorer** (sectionnée par méta-catégorie)
- Nouvelle page **Accueil** à créer (feed curaté, plusieurs rows)
- Nouvelle page **Recherche** à créer
- Pas de backend ni d'indexation nécessaire : tout reste local, basé sur l'enum `ContentType` existant et `shared_preferences` pour le tracking "récemment visité"

---

## Prochaines étapes

1. Trancher les méta-catégories définitives (dépend de l'avancement du chantier [new-categories](../new-categories/TECH_PLAN.md))
2. Détailler le contenu exact de chaque row de l'Accueil
3. Maquetter (design) avant tout code, vu que c'est un changement structurant visible immédiatement par tous les utilisateurs
