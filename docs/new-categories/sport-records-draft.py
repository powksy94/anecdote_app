# BROUILLON — Records sportifs (sous-catégorie "Univers" du hub Sport)
# 91 entrées, jugé suffisant le 2026-09-28 (objectif ~100 abandonné, la diversité de sports/pays
# prime sur le compte rond). Relecture faite : athlétisme réduit de 17 à 10 entrées, diversité
# géographique renforcée (Asie du Sud/Est notamment). Reste à faire avant tout code : dernière
# passe de relecture libre si besoin, puis rédaction du script tools/sport/generate_sport_records.py.
# Chaque entrée listée a été vérifiée via recherche web (pas seulement la mémoire du modèle) le 2026-09-28,
# sauf mention contraire. Structure : n=nom du record, sp=sport, hd=détenteur (personne ou équipe),
# cc=code ISO2 (None si équipe/duo multinational), yr=année, fa=fait/contexte (pas de tiret —).

records = [
    # ── Lot 1 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "Le premier marathon officiel sous les deux heures", "sp": "Athlétisme (marathon)", "hd": "Sabastian Sawe", "cc": "KE", "yr": "2026",
     "fa": "1h59:30 au marathon de Londres, devenant le premier coureur à passer sous la barre des deux heures dans une course officielle homologuée. Il améliore de plus d'une minute le précédent record de Kelvin Kiptum."},

    {"n": "Le marathon le plus rapide jamais couru par une femme", "sp": "Athlétisme (marathon)", "hd": "Ruth Chepngetich", "cc": "KE", "yr": "2024",
     "fa": "2h09:56 à Chicago, dans une course mixte, restant à ce jour la performance la plus rapide toutes catégories confondues chez les femmes."},

    {"n": "Le record du monde du 100 m", "sp": "Athlétisme (sprint)", "hd": "Usain Bolt", "cc": "JM", "yr": "2009",
     "fa": "9,58 secondes aux Championnats du monde de Berlin, un temps que personne n'a réussi à approcher à moins de deux dixièmes depuis plus de quinze ans."},

    {"n": "Le service le plus rapide jamais enregistré au tennis", "sp": "Tennis", "hd": "Sam Groth", "cc": "AU", "yr": "2012",
     "fa": "263,4 km/h lors d'un tournoi Challenger à Busan. Il reste le plus rapide jamais chronométré, même si l'ATP ne le reconnaît pas comme record officiel du circuit, les radars des tournois Challenger n'étant pas soumis aux mêmes normes de calibration."},

    {"n": "Le plus long match de tennis de l'histoire", "sp": "Tennis", "hd": "John Isner & Nicolas Mahut", "cc": None, "yr": "2010",
     "fa": "11 heures et 5 minutes de jeu à Wimbledon, étalées sur trois jours, pour un score final de 70 jeux à 68 au 5e set. Ce record est aujourd'hui inégalable : Wimbledon a depuis instauré un jeu décisif à 12-12 dans les sets décisifs."},

    {"n": "Le plus long saut à ski jamais réalisé", "sp": "Saut à ski", "hd": "Domen Prevc", "cc": "SI", "yr": "2025",
     "fa": "254,5 mètres à Planica, améliorant d'un mètre le record vieux de huit ans de l'Autrichien Stefan Kraft."},

    {"n": "Le plus jeune champion du monde de Formule 1", "sp": "Formule 1", "hd": "Sebastian Vettel", "cc": "DE", "yr": "2010",
     "fa": "23 ans lors de son premier titre, décroché à la toute dernière course de la saison après avoir devancé trois autres pilotes encore en course pour le titre ce jour-là."},

    {"n": "La seule carrière de boxe professionnelle parfaite chez les poids lourds", "sp": "Boxe", "hd": "Rocky Marciano", "cc": "US", "yr": "1956",
     "fa": "49 victoires en 49 combats à sa retraite, le seul champion du monde des poids lourds à n'avoir jamais connu la défaite."},

    {"n": "Le total le plus lourd jamais soulevé en haltérophilie olympique", "sp": "Haltérophilie", "hd": "Lasha Talakhadze", "cc": "GE", "yr": "2021",
     "fa": "488 kg cumulés à l'arraché et à l'épaulé-jeté aux Jeux de Tokyo, améliorant son propre record du monde en pleine compétition."},

    {"n": "Le plus de home runs en une saison de baseball", "sp": "Baseball", "hd": "Barry Bonds", "cc": "US", "yr": "2001",
     "fa": "73 home runs avec les San Francisco Giants, un record qui reste controversé en raison de soupçons de dopage jamais totalement clarifiés."},

    {"n": "Le record du monde du 100 m nage libre (hommes)", "sp": "Natation", "hd": "Pan Zhanle", "cc": "CN", "yr": "2024",
     "fa": "46,40 secondes établies aux Jeux de Paris, pulvérisant un record qui semblait pourtant indépassable depuis l'interdiction des combinaisons intégrales en 2010."},

    {"n": "La plus longue série de victoires en NBA", "sp": "Basketball", "hd": "Los Angeles Lakers", "cc": "US", "yr": "1972",
     "fa": "33 victoires consécutives lors de la saison 1971-1972, une série qui a duré plus de deux mois sans la moindre défaite et n'a jamais été approchée depuis."},

    {"n": "Le record de l'heure en cyclisme sur piste", "sp": "Cyclisme", "hd": "Filippo Ganna", "cc": "IT", "yr": "2022",
     "fa": "56,792 km parcourus en une heure sur le vélodrome de Grenchen, la distance la plus longue jamais couverte sur cette épreuve mythique."},

    # ── Lot 2 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "Le record du monde du saut à la perche", "sp": "Athlétisme (saut à la perche)", "hd": "Armand \"Mondo\" Duplantis", "cc": "SE", "yr": "2026",
     "fa": "6,31 mètres franchis en Suède, la 15e fois qu'il bat son propre record depuis 2020, généralement en l'améliorant d'un centimètre à chaque tentative."},

    {"n": "Le record du monde du saut en hauteur", "sp": "Athlétisme (saut en hauteur)", "hd": "Javier Sotomayor", "cc": "CU", "yr": "1993",
     "fa": "2,45 mètres franchis à Salamanque, le record le plus ancien encore en vigueur en athlétisme masculin, invaincu depuis plus de 30 ans."},

    {"n": "Le plus grand score individuel de l'histoire du cricket test", "sp": "Cricket", "hd": "Brian Lara", "cc": "TT", "yr": "2004",
     "fa": "400 points marqués sans être éliminé contre l'Angleterre, en battant pendant près de trois jours. Il reste le seul joueur à avoir dépassé la barre symbolique des 400 dans l'histoire du cricket test."},

    {"n": "Le plus de buts marqués en une année civile au football", "sp": "Football", "hd": "Lionel Messi", "cc": "AR", "yr": "2012",
     "fa": "91 buts marqués avec le FC Barcelone et la sélection argentine, un total officiellement reconnu par la Fédération internationale d'histoire et de statistiques du football comme record de l'ère moderne."},

    {"n": "L'olympien le plus médaillé de l'histoire", "sp": "Natation", "hd": "Michael Phelps", "cc": "US", "yr": "2016",
     "fa": "28 médailles olympiques au total sur cinq éditions des Jeux, dont 23 en or. Aucun autre athlète, dans aucun sport, n'a jamais approché ce total."},

    {"n": "Le plus grand nombre de points marqués dans un match de NBA", "sp": "Basketball", "hd": "Wilt Chamberlain", "cc": "US", "yr": "1962",
     "fa": "100 points inscrits en un seul match face aux New York Knicks, un exploit individuel jamais égalé depuis plus de 60 ans."},

    # ── Lot 3 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "Le plus bas score cumulé sur 72 trous dans un tournoi majeur de golf", "sp": "Golf", "hd": "Xander Schauffele", "cc": "US", "yr": "2024",
     "fa": "263 coups (21 sous le par) au Championnat PGA de Valhalla, le meilleur total jamais réalisé sur les quatre tournois majeurs masculins."},

    {"n": "Le plus de yards à la course en une saison de NFL", "sp": "Football américain", "hd": "Eric Dickerson", "cc": "US", "yr": "1984",
     "fa": "2 105 yards parcourus au sol en une seule saison régulière, un record qui résiste depuis plus de 40 ans malgré l'évolution du jeu vers des attaques toujours plus axées sur la passe."},

    {"n": "Le record du monde du 500 m en patinage de vitesse", "sp": "Patinage de vitesse", "hd": "Pavel Kulizhnikov", "cc": "RU", "yr": "2019",
     "fa": "33,61 secondes établies à Salt Lake City, une piste située en haute altitude qui offre un air plus fin et donc moins de résistance, ce qui en fait le terrain de jeu privilégié des records de vitesse sur glace."},

    # ── Lot 4 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "L'humain le plus rapide sur des skis", "sp": "Ski de vitesse", "hd": "Simon Billy", "cc": "FR", "yr": "2023",
     "fa": "255,5 km/h atteints en ligne droite, une discipline distincte du ski alpin classique où les skieurs ne cherchent qu'à atteindre la vitesse maximale sur une pente dédiée, sans aucune porte à négocier."},

    {"n": "Le plus jeune champion du monde d'échecs de l'histoire", "sp": "Échecs", "hd": "Gukesh Dommaraju", "cc": "IN", "yr": "2024",
     "fa": "18 ans lors de son sacre face à Ding Liren, battant le record de précocité que détenait Garry Kasparov depuis 1985, où il avait été sacré à 22 ans."},

    {"n": "Le plus haut break jamais réalisé au snooker en compétition", "sp": "Snooker", "hd": "Ronnie O'Sullivan", "cc": "GB", "yr": "2026",
     "fa": "153 points inscrits sur une seule visite de table lors du World Open, plus que le maximum théorique de 147 habituellement considéré comme la limite absolue, rendu possible par une situation rare de bille libre (free ball)."},

    {"n": "Le plus de yards à la passe en carrière en NFL", "sp": "Football américain", "hd": "Tom Brady", "cc": "US", "yr": "2022",
     "fa": "89 214 yards parcourus par ses passes sur 23 saisons de carrière, en plus du record du nombre de passes de touchdown (738), aucun autre quarterback n'ayant approché cette longévité au plus haut niveau."},

    # ── Lot 5 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "Le smash le plus rapide jamais mesuré au badminton", "sp": "Badminton", "hd": "Satwiksairaj Rankireddy", "cc": "IN", "yr": "2023",
     "fa": "565 km/h mesurés en conditions de laboratoire chez le fabricant Yonex au Japon, largement au-dessus de la vitesse de n'importe quel service au tennis ou smash au volley-ball."},

    {"n": "Le plus de buts marqués en une seule saison de NHL", "sp": "Hockey sur glace", "hd": "Wayne Gretzky", "cc": "CA", "yr": "1982",
     "fa": "92 buts inscrits lors de la saison 1981-1982, un total resté hors de portée depuis plus de 40 ans malgré les tentatives des meilleurs buteurs de chaque génération."},

    {"n": "Le plus grand nombre de buts en carrière dans l'histoire de la NHL", "sp": "Hockey sur glace", "hd": "Alexander Ovechkin", "cc": "RU", "yr": "2025",
     "fa": "895e but de carrière inscrit le 6 avril 2025, dépassant un record que détenait Wayne Gretzky depuis 31 ans. Les deux joueurs avaient inscrit ce total en exactement le même nombre de matchs, 1 487."},

    # ── Lot 6 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "Le premier 501 en neuf fléchettes lors d'un Championnat du monde", "sp": "Fléchettes", "hd": "Paul Lim", "cc": "US", "yr": "1990",
     "fa": "Neuf fléchettes lancées pour effacer 501 points, la partie parfaite au jeu des fléchettes, réalisée pour la première fois en Championnat du monde face à l'Irlandais Jack McKenna."},

    {"n": "Le plus de victoires au Tour de France", "sp": "Cyclisme", "hd": "Tadej Pogačar", "cc": "SI", "yr": "2026",
     "fa": "5e victoire au général en 2026, rejoignant un club très fermé où figurent déjà Jacques Anquetil, Eddy Merckx, Bernard Hinault et Miguel Indurain, désormais à égalité à cinq titres chacun."},

    {"n": "Le record du monde du 400 m", "sp": "Athlétisme (sprint)", "hd": "Wayde van Niekerk", "cc": "ZA", "yr": "2016",
     "fa": "43,03 secondes courues aux Jeux de Rio, dans le couloir 8 où il ne pouvait voir aucun de ses adversaires pendant toute la course."},

    # ── Lot 7 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "La gymnaste la plus médaillée d'or aux Jeux olympiques", "sp": "Gymnastique", "hd": "Larisa Latynina", "cc": "UA", "yr": "1964",
     "fa": "9 médailles d'or olympiques accumulées entre 1956 et 1964, un record qui a résisté à toutes les générations suivantes de gymnastes, y compris Simone Biles."},

    {"n": "Le plus de victoires en catégorie reine du championnat du monde de vitesse moto", "sp": "Moto (MotoGP)", "hd": "Valentino Rossi", "cc": "IT", "yr": "2026",
     "fa": "89 victoires en catégorie reine (500cc puis MotoGP) sur une carrière de plus de 20 ans, un total que même Marc Marquez, deuxième de l'histoire, n'a toujours pas réussi à atteindre."},

    {"n": "Le jeu parfait le plus rapide de l'histoire du bowling", "sp": "Bowling", "hd": "Ben Ketola", "cc": "US", "yr": "2017",
     "fa": "300 points parfaits enchaînés en moins de 90 secondes, chaque boule étant relancée dès la précédente terminée, un rythme jugé presque impossible à tenir sans la moindre erreur de visée."},

    # ── Lot 8 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "Le plus grand buteur de l'histoire de la Coupe du monde de football", "sp": "Football", "hd": "Kylian Mbappé", "cc": "FR", "yr": "2026",
     "fa": "22 buts inscrits en Coupe du monde à l'issue de l'édition 2026, dépassant Lionel Messi (21) lors de la petite finale. Les deux joueurs s'étaient échangé la place de meilleur buteur de l'histoire à plusieurs reprises durant le même tournoi."},

    {"n": "Le record du monde du 100 m brasse", "sp": "Natation", "hd": "Adam Peaty", "cc": "GB", "yr": "2019",
     "fa": "56,88 secondes établies aux Championnats du monde de Gwangju, le seul nageur de l'histoire à être passé sous la barre symbolique des 57 secondes sur cette distance."},

    {"n": "Le record du monde du 100 m dos", "sp": "Natation", "hd": "Thomas Ceccon", "cc": "IT", "yr": "2022",
     "fa": "51,60 secondes établies aux Championnats du monde de Budapest, améliorant d'un coup le précédent record de plus de trois dixièmes de seconde, un écart énorme à ce niveau de compétition."},

    # ── Lot 9 (vérifié 2026-09-28) ──────────────────────────────────────────
    {"n": "Le plus de titres du Grand Chelem toutes catégories confondues", "sp": "Tennis", "hd": "Margaret Court", "cc": "AU", "yr": "1975",
     "fa": "64 titres remportés entre 1960 et 1975, répartis entre 24 titres en simple, 19 en double dames et 21 en double mixte, un total qu'aucun joueur ou joueuse n'a jamais approché depuis."},

    # ── Lot 10 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le record du monde d'escalade de vitesse", "sp": "Escalade", "hd": "Zhao Yicheng", "cc": "CN", "yr": "2026",
     "fa": "4,54 secondes pour grimper un mur de 15 mètres, établies à seulement 16 ans lors d'une compétition en Chine, quelques semaines après avoir déjà battu son propre record précédent."},

    {"n": "Le skieur de fond le plus médaillé d'or aux Jeux olympiques d'hiver", "sp": "Ski de fond", "hd": "Johannes Høsflot Klæbo", "cc": "NO", "yr": "2026",
     "fa": "11 médailles d'or olympiques au total après les Jeux de Milan-Cortina, où il a remporté l'or dans les six épreuves auxquelles il a participé. Il ne reste devant lui que le nageur Michael Phelps, seul athlète, toutes disciplines confondues, à avoir fait mieux."},

    {"n": "Le record du monde d'aviron en skiff (2000 m)", "sp": "Aviron", "hd": "Simon van Dorp", "cc": "NL", "yr": "2026",
     "fa": "5 minutes et 33,4 secondes, devenant le premier rameur à descendre sous la barre des 5:34, à peine quelques semaines après que le record avait déjà été battu par le champion olympique Oliver Zeidler."},

    # ── Lot 11 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le smash le plus rapide jamais mesuré au tennis de table", "sp": "Tennis de table", "hd": "Łukasz Budner", "cc": "PL", "yr": "2016",
     "fa": "116 km/h enregistrés lors d'un championnat en Pologne, une vitesse presque impossible à suivre à l'œil nu sur une table de moins de trois mètres de long."},

    {"n": "Le plus de points marqués sur un tour de 1440 en tir à l'arc compound", "sp": "Tir à l'arc", "hd": "Mike Schloesser", "cc": "NL", "yr": "2026",
     "fa": "1 421 points sur un maximum de 1 440, obtenus aux Pays-Bas sur une compétition de 144 flèches tirées à des distances allant de 30 à 90 mètres."},

    {"n": "Le lutteur le plus médaillé d'or aux Jeux olympiques", "sp": "Lutte", "hd": "Mijaín López", "cc": "CU", "yr": "2024",
     "fa": "5 médailles d'or consécutives obtenues entre 2008 et 2024, dans deux catégories de poids différentes, un règne olympique individuel de 16 ans qu'aucun autre lutteur n'a jamais égalé."},

    {"n": "Le set de volley-ball le plus long de l'histoire olympique", "sp": "Volley-ball", "hd": "Italie & Argentine", "cc": None, "yr": "2000",
     "fa": "L'Italie s'est imposée 40 points à 38 face à l'Argentine à Sydney, un set si long qu'il reste la référence absolue près de 25 ans plus tard, la règle des sets à avantages ayant depuis été resserrée dans plusieurs compétitions."},

    # ── Lot 12 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le record du monde du lancer de marteau", "sp": "Athlétisme (lancer)", "hd": "Yuriy Sedykh", "cc": "RU", "yr": "1986",
     "fa": "86,74 mètres lancés à Stuttgart, le plus ancien record du monde masculin encore en vigueur en athlétisme, établi près de quarante ans plus tôt à l'époque de l'URSS."},

    {"n": "Le record du monde du 800 m", "sp": "Athlétisme (demi-fond)", "hd": "David Rudisha", "cc": "KE", "yr": "2012",
     "fa": "1 minute 40,91 secondes courues à la régularité parfaite aux Jeux de Londres, où il a couru le premier et le second tour presque exactement au même rythme, une prouesse tactique jugée irréalisable sur cette distance."},

    {"n": "Le plus de titres à l'Open britannique de squash", "sp": "Squash", "hd": "Jahangir Khan", "cc": "PK", "yr": "1991",
     "fa": "10 titres consécutifs remportés entre 1982 et 1991, lors d'une période où il est resté invaincu en compétition officielle pendant plus de cinq ans, l'une des plus longues séries d'invincibilité individuelles de tous les sports."},

    # ── Lot 13 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "La plus grande vague jamais surfée", "sp": "Surf", "hd": "Sebastian Steudtner", "cc": "DE", "yr": "2020",
     "fa": "26,21 mètres de haut à Nazaré au Portugal, un spot connu pour son canyon sous-marin qui amplifie la houle de l'Atlantique jusqu'à créer des murs d'eau records chaque hiver."},

    {"n": "Le plus de buts marqués en water-polo aux Jeux olympiques", "sp": "Water-polo", "hd": "Manuel Estiarte", "cc": "ES", "yr": "1996",
     "fa": "127 buts inscrits sur six participations olympiques entre 1980 et 1996, une longévité exceptionnelle pour un sport aussi physique, disputé en immersion quasi permanente."},

    {"n": "Le premier 1080 réalisé sur une rampe verticale en skateboard", "sp": "Skateboard", "hd": "Gui Khury", "cc": "BR", "yr": "2020",
     "fa": "Trois rotations complètes en l'air à seulement 11 ans, battant le record de Tony Hawk qui avait mis douze tentatives pour réussir 900 degrés en 1999, soit une rotation de moins."},

    # ── Lot 14 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "L'escrimeur le plus médaillé de l'histoire olympique", "sp": "Escrime", "hd": "Edoardo Mangiarotti", "cc": "IT", "yr": "1960",
     "fa": "13 médailles olympiques au total (6 en or, 5 en argent, 2 en bronze) glanées entre 1936 et 1960, une carrière étalée sur plus de deux décennies malgré l'interruption des Jeux pendant la Seconde Guerre mondiale."},

    {"n": "Le plus de titres mondiaux de judo remportés par un individu", "sp": "Judo", "hd": "Teddy Riner", "cc": "FR", "yr": "2023",
     "fa": "12 titres mondiaux glanés entre 2009 et 2023, dont neuf dans sa catégorie de poids et deux en toutes catégories confondues, un record qu'aucun autre judoka de l'histoire n'a jamais approché."},

    {"n": "Le saut le plus haut jamais réalisé en BMX", "sp": "BMX", "hd": "Mat Hoffman", "cc": "US", "yr": "2001",
     "fa": "8,07 mètres de haut à partir d'une rampe de 7,31 mètres, avec un élan pris en étant tracté par une moto pour atteindre une vitesse impossible à générer en pédalant seul."},

    # ── Lot 15 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "La vitesse la plus élevée jamais enregistrée en luge", "sp": "Luge", "hd": "Felix Loch", "cc": "DE", "yr": "2009",
     "fa": "153,98 km/h atteints sur la piste de Whistler au Canada, allongé sur un traîneau à quelques centimètres de la glace, sans aucun système de freinage avant la ligne d'arrivée."},

    {"n": "Le plus haut saut jamais réalisé par un cheval en compétition officielle", "sp": "Équitation (saut d'obstacles)", "hd": "Huaso (cheval monté par Alberto Larraguibel)", "cc": "CL", "yr": "1949",
     "fa": "2,47 mètres franchis au Chili, un record resté invaincu depuis plus de 75 ans et officiellement reconnu par la Fédération équestre internationale comme le plus haut jamais homologué."},

    {"n": "Le plus de médailles d'or olympiques en canoë-kayak", "sp": "Canoë-kayak", "hd": "Birgit Fischer & Lisa Carrington", "cc": None, "yr": "2024",
     "fa": "8 titres olympiques chacune, un record partagé depuis 2024 entre l'Allemande Birgit Fischer, retraitée depuis 20 ans, et la Néo-Zélandaise Lisa Carrington, venue l'égaler à Paris."},

    # ── Lot 16 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le plus haut saut de falaise jamais réalisé", "sp": "Cliff diving", "hd": "Laso Schaller", "cc": "CH", "yr": "2015",
     "fa": "58,5 mètres de chute depuis une cascade en Suisse. Techniquement un saut et non un plongeon : contrairement au plongeon classique, les pieds touchent l'eau en premier, sans rotation à 180 degrés."},

    {"n": "La plus longue série sans défaite en Serie A italienne", "sp": "Football", "hd": "AC Milan", "cc": "IT", "yr": "1993",
     "fa": "58 matchs sans défaite entre mai 1991 et mars 1993 sous la direction de Fabio Capello, une domination qui a valu à cette équipe le surnom des \"Invincibles\"."},

    # ── Lot 17 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le plus de titres remportés dans l'histoire du sumo", "sp": "Sumo", "hd": "Hakuho Sho", "cc": "MN", "yr": "2021",
     "fa": "45 titres de champion dans la division suprême entre 2006 et 2021, dont 16 tournois remportés sans la moindre défaite, un total qui dépasse de 13 le précédent record établi par la légende Taiho."},

    {"n": "Le plus long but sur coup de pied placé de l'histoire de la NFL", "sp": "Football américain", "hd": "Cam Little", "cc": "US", "yr": "2025",
     "fa": "68 yards, soit plus de 62 mètres, réussis en saison régulière face aux Raiders. Il détient aussi le deuxième plus long avec un tir à 67 yards la même saison."},

    {"n": "Le plus de paniers à 3 points marqués en carrière en NBA", "sp": "Basketball", "hd": "Stephen Curry", "cc": "US", "yr": "2021",
     "fa": "Record battu le 14 décembre 2021 en dépassant Ray Allen, qui assistait au match et est venu le féliciter sur le terrain à l'arrêt du jeu. Curry continue d'allonger son propre total à chaque saison depuis."},

    # ── Lot 18 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le record du monde du 3000 m steeple", "sp": "Athlétisme (steeple)", "hd": "Lamecha Girma", "cc": "ET", "yr": "2023",
     "fa": "7 minutes 52,11 secondes à franchir 28 haies et 7 rivières artificielles, la discipline d'athlétisme la plus technique où l'endurance doit composer avec l'obstacle à chaque tour de piste."},

    {"n": "La plus longue série d'invincibilité dans l'histoire du sport", "sp": "Voile", "hd": "New York Yacht Club", "cc": "US", "yr": "1983",
     "fa": "25 défenses victorieuses consécutives de la Coupe de l'America entre 1851 et 1983, soit 132 ans sans jamais perdre le trophée, l'une des dominations les plus longues jamais enregistrées, toutes disciplines sportives confondues."},

    {"n": "La vitesse la plus élevée jamais atteinte en drag racing", "sp": "Drag racing", "hd": "Brittany Force", "cc": "US", "yr": "2025",
     "fa": "552,85 km/h (343,51 mph) parcourus sur 305 mètres de piste en moins de 4 secondes, dans un dragster Top Fuel propulsé par un moteur qui consomme plus de carburant en une course qu'une voiture de ville en plusieurs années."},

    # ── Lot 19 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le record du monde du 100 m papillon (femmes)", "sp": "Natation", "hd": "Gretchen Walsh", "cc": "US", "yr": "2026",
     "fa": "54,33 secondes établies en Floride, la quatrième fois qu'elle bat son propre record depuis juin 2024. Elle détient à elle seule les 13 temps les plus rapides jamais enregistrés sur cette distance."},

    {"n": "Le biathlète le plus médaillé de l'histoire olympique", "sp": "Biathlon", "hd": "Ole Einar Bjørndalen", "cc": "NO", "yr": "2014",
     "fa": "13 médailles olympiques au total, dont 8 en or, glanées sur une carrière longue de 18 ans. Aux Jeux de Salt Lake City 2002, il a remporté les trois épreuves individuelles et le relais, un quadruplé jamais réalisé depuis."},

    {"n": "Le plus grand score individuel de l'histoire du cricket en ODI", "sp": "Cricket", "hd": "Rohit Sharma", "cc": "IN", "yr": "2014",
     "fa": "264 points marqués en une seule manche face au Sri Lanka, sur seulement 173 balles, le seul joueur à avoir dépassé les 260 points dans un match international en un jour."},

    # ── Lot 20 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le record du monde du relais 4x100 m", "sp": "Athlétisme (relais)", "hd": "Jamaïque (Bolt, Blake, Carter, Frater)", "cc": "JM", "yr": "2012",
     "fa": "36,84 secondes courues aux Jeux de Londres avec Usain Bolt en dernier relayeur, un record que même les meilleures équipes actuelles n'ont jamais réussi à approcher depuis plus de dix ans."},

    {"n": "Le plus de buts marqués en sélection nationale dans l'histoire du football", "sp": "Football", "hd": "Cristiano Ronaldo", "cc": "PT", "yr": "2026",
     "fa": "146 buts inscrits avec le Portugal, le total le plus élevé jamais enregistré en équipe nationale, toutes nations confondues, dans l'histoire du football international."},

    {"n": "La nation la plus titrée en hockey sur gazon aux Jeux olympiques", "sp": "Hockey sur gazon", "hd": "Inde", "cc": "IN", "yr": "1980",
     "fa": "8 médailles d'or remportées entre 1928 et 1980, dont six consécutives entre 1928 et 1956, une domination sans équivalent dans l'histoire du sport olympique par équipe."},

    # ── Lot 21 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "La plus longue partie d'échecs jamais jouée", "sp": "Échecs", "hd": "Ivan Nikolić & Goran Arsović", "cc": None, "yr": "1989",
     "fa": "269 coups joués à Belgrade sur près de 20 heures de jeu, avant de se conclure sur un match nul grâce à la règle des 50 coups sans capture ni mouvement de pion."},

    {"n": "Le score parfait le plus rare du curling", "sp": "Curling", "hd": None, "cc": None, "yr": "2026",
     "fa": "Réussir un \"eight-ender\" (les huit pierres d'une équipe marquantes sur une seule manche) a une probabilité estimée à 1 sur 120 000 en curling amateur, un exploit plus rare qu'un trou en un au golf ou qu'une partie parfaite au bowling."},

    {"n": "Le plus de titres à Wimbledon en simple messieurs", "sp": "Tennis", "hd": "Roger Federer", "cc": "CH", "yr": "2017",
     "fa": "8 titres remportés entre 2003 et 2017. Il est aussi le seul joueur, toutes époques confondues, à avoir atteint douze fois la finale du tournoi."},

    # ── Lot 22 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le plus de pole positions en Formule 1", "sp": "Formule 1", "hd": "Lewis Hamilton", "cc": "GB", "yr": "2021",
     "fa": "105 pole positions en carrière, devenant le premier pilote à franchir la barre symbolique des 100 lors du Grand Prix d'Espagne 2021, après avoir dépassé le record de Michael Schumacher quatre ans plus tôt."},

    {"n": "Le plus de triple-doubles en carrière dans l'histoire de la NBA", "sp": "Basketball", "hd": "Russell Westbrook", "cc": "US", "yr": "2026",
     "fa": "209 triple-doubles au moment de sa retraite en août 2026, un record qu'il avait pris à Oscar Robertson en 2021 et qui pourrait bien être le prochain à tomber face à Nikola Jokić."},

    # ── Lot 23 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le plus de titres du Super Bowl remportés par un joueur", "sp": "Football américain", "hd": "Tom Brady", "cc": "US", "yr": "2021",
     "fa": "7 bagues de champion remportées, six avec les New England Patriots puis une septième à 43 ans avec les Tampa Bay Buccaneers. Aucun autre joueur de l'histoire n'en a remporté plus de cinq."},

    {"n": "Le plus de guichets pris dans l'histoire du cricket test", "sp": "Cricket", "hd": "Muttiah Muralitharan", "cc": "LK", "yr": "2010",
     "fa": "800 guichets exactement, un total atteint sur sa toute dernière balle de sa toute dernière rencontre en carrière face à l'Inde, un scénario si parfait qu'il semble scénarisé."},

    # ── Lot 24 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le club le plus titré en Ligue des champions", "sp": "Football", "hd": "Real Madrid", "cc": "ES", "yr": "2024",
     "fa": "15 titres au total, dont cinq consécutifs entre 1956 et 1960 lors de la toute première décennie de la compétition, un début de domination jamais égalé depuis par aucun autre club."},

    {"n": "Le plus de home runs en carrière dans l'histoire du baseball", "sp": "Baseball", "hd": "Barry Bonds", "cc": "US", "yr": "2007",
     "fa": "762 home runs au total, un record atteint le 7 août 2007 en dépassant Hank Aaron, dans une carrière tout aussi marquée par les soupçons de dopage que par les statistiques elles-mêmes."},

    {"n": "La plus longue série de victoires consécutives au tennis (ère Open)", "sp": "Tennis", "hd": "Guillermo Vilas", "cc": "AR", "yr": "1977",
     "fa": "46 matchs gagnés d'affilée en 1977, le record officiellement reconnu par l'ATP. Björn Borg revendique des séries encore plus longues la même période, mais elles incluent des matchs par forfait non comptabilisés par l'ATP."},

    # ── Lot 25 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le plus de titres NBA remportés par un joueur", "sp": "Basketball", "hd": "Bill Russell", "cc": "US", "yr": "1969",
     "fa": "11 titres remportés en 13 saisons avec les Boston Celtics entre 1957 et 1969, dont huit consécutifs, un record d'équipe sportive qui reste totalement hors de portée dans n'importe quel sport aujourd'hui."},

    {"n": "Le plus de victoires d'étape au Tour de France", "sp": "Cyclisme", "hd": "Mark Cavendish", "cc": "GB", "yr": "2024",
     "fa": "35 victoires d'étape au compteur après le Tour 2024, dépassant le record vieux de plusieurs décennies d'Eddy Merckx, qui en comptait 34."},

    {"n": "Le plus de buts marqués en sélection nationale dans l'histoire du football féminin", "sp": "Football", "hd": "Christine Sinclair", "cc": "CA", "yr": "2020",
     "fa": "190 buts inscrits avec le Canada, un total qui dépasse même le record masculin toutes nations confondues. Elle a battu le précédent record d'Abby Wambach lors d'un match de qualification olympique remporté 11 à 0."},

    # ── Lot 26 (vérifié 2026-09-28) ─────────────────────────────────────────
    {"n": "Le plus de buts marqués par un joueur lors d'une seule Coupe du monde", "sp": "Football", "hd": "Just Fontaine", "cc": "FR", "yr": "1958",
     "fa": "13 buts inscrits en Suède, plus du double du deuxième meilleur buteur du tournoi. Il a joué toute la compétition avec des crampons empruntés à un coéquipier, n'ayant pas les siens à sa taille."},

    {"n": "Le plus long temps sans encaisser de but pour un gardien de football", "sp": "Football", "hd": "Abel Resino", "cc": "ES", "yr": "1991",
     "fa": "14 matchs et 15 minutes sans encaisser le moindre but avec l'Atlético Madrid, le record absolu toutes compétitions confondues pour un gardien de but."},

    # ── Lot 27 (vérifié 2026-09-28) — Asie du Sud et de l'Est ───────────────
    {"n": "Le seul boxeur champion du monde dans huit catégories de poids différentes", "sp": "Boxe", "hd": "Manny Pacquiao", "cc": "PH", "yr": "2010",
     "fa": "12 titres mondiaux glanés entre 48 et 70 kg, du poids mouche au super mi-moyen. Aucun autre boxeur de l'histoire n'a jamais été champion du monde dans plus de quatre catégories différentes."},

    {"n": "L'invincibilité la plus longue en tir à l'arc par équipe aux Jeux olympiques", "sp": "Tir à l'arc", "hd": "Corée du Sud (équipe féminine)", "cc": "KR", "yr": "2024",
     "fa": "Invaincue depuis l'introduction de l'épreuve par équipe en 1988, visant un 10e titre consécutif. La Corée du Sud cumule à elle seule 43 médailles olympiques en tir à l'arc, 13 de plus que les États-Unis, deuxièmes."},

    {"n": "Le plus de coups sûrs en carrière dans le baseball professionnel", "sp": "Baseball", "hd": "Ichiro Suzuki", "cc": "JP", "yr": "2016",
     "fa": "4 257 coups sûrs cumulés entre le championnat japonais (NPB) et la MLB, dépassant le record de Pete Rose. Il détient aussi le record du nombre de coups sûrs en une seule saison MLB avec 262 en 2004."},

    {"n": "La nation la plus titrée à la Coupe Thomas de badminton", "sp": "Badminton", "hd": "Indonésie", "cc": "ID", "yr": "2020",
     "fa": "14 titres remportés depuis la création de la compétition par équipe masculine en 1948, dont deux séries de quatre et cinq titres consécutifs, devant la Chine qui en compte 12."},
]

# Pistes explorées puis écartées faute de source fiable et cohérente (sources contradictoires) :
# - Record du nombre d'essais en rugby international : sources divergentes entre Daisuke Ohata (69),
#   Bryan Habana (67) et Damian Penaud (record français, pas mondial) — à re-vérifier plus tard avec une
#   source arbitrale unique avant de l'inclure.
# - Record Ironman/triathlon longue distance : Ironman a confirmé en 2026 ne tenir aucun "record du monde"
#   officiel (parcours non certifiés, non comparables d'une course à l'autre) — écarté, pas de record fiable à citer.
# - Record du nombre de défenses de titre en UFC : sources contradictoires sur le total exact de Jon Jones
#   (11 vs 13 selon les sources) — à re-vérifier avec une source unique avant de l'inclure.

# Faits initialement rédigés de mémoire puis trouvés PÉRIMÉS lors de la vérification 2026-09-28
# (conservé ici pour ne pas refaire la même erreur si le sujet revient) :
# - Saut à ski : Stefan Kraft 253,5m (2017) -> en réalité battu par Domen Prevc 254,5m (mars 2025)
# - 100m nage libre : César Cielo 46,91s (2009) -> en réalité battu par Pan Zhanle 46,40s (2024)
# - Record de l'heure cyclisme : référence à Eddy Merckx -> le record actuel est Filippo Ganna (2022)
