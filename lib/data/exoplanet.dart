import 'dart:convert';
import 'package:flutter/services.dart';

class Exoplanet {
  final String name;        // Nom de la planète
  final String host;        // Étoile hôte
  final String method;      // Méthode de découverte
  final String year;        // Année de découverte
  final String facility;    // Observatoire
  final double? orbper;     // Période orbitale (jours)
  final double? rade;       // Rayon en rayons terrestres
  final double? radj;       // Rayon en rayons joviens
  final double? masse;      // Masse en masses terrestres
  final double? eqt;        // Température d'équilibre (K)
  final String spectype;    // Type spectral de l'étoile
  final double? steff;      // Température de l'étoile (K)
  final String rastr;       // Ascension droite (texte ex: 12h20m42s)
  final double? ra;         // Ascension droite (degrés)
  final String decstr;      // Déclinaison (texte ex: +17d47m35s)
  final double? dec;        // Déclinaison (degrés)
  final double? dist;       // Distance (parsecs)

  const Exoplanet({
    required this.name,
    required this.host,
    required this.method,
    required this.year,
    required this.facility,
    this.orbper,
    this.rade,
    this.radj,
    this.masse,
    this.eqt,
    required this.spectype,
    this.steff,
    required this.rastr,
    this.ra,
    required this.decstr,
    this.dec,
    this.dist,
  });

  factory Exoplanet.fromJson(Map<String, dynamic> j) => Exoplanet(
        name:     j['n']  as String? ?? '',
        host:     j['h']  as String? ?? '',
        method:   j['m']  as String? ?? '',
        year:     j['y']  as String? ?? '',
        facility: j['f']  as String? ?? '',
        orbper:   (j['op'] as num?)?.toDouble(),
        rade:     (j['re'] as num?)?.toDouble(),
        radj:     (j['rj'] as num?)?.toDouble(),
        masse:    (j['me'] as num?)?.toDouble(),
        eqt:      (j['t']  as num?)?.toDouble(),
        spectype: j['sp'] as String? ?? '',
        steff:    (j['st'] as num?)?.toDouble(),
        rastr:    j['rs'] as String? ?? '',
        ra:       (j['ra'] as num?)?.toDouble(),
        decstr:   j['ds'] as String? ?? '',
        dec:      (j['dc'] as num?)?.toDouble(),
        dist:     (j['d']  as num?)?.toDouble(),
      );
}

/// Charge la liste complète depuis l'asset JSON.
/// À appeler une seule fois au démarrage et mettre en cache.
Future<List<Exoplanet>> loadExoplanets() async {
  final raw = await rootBundle.loadString('assets/exoplanets.json');
  final list = jsonDecode(raw) as List<dynamic>;
  return list.map((e) => Exoplanet.fromJson(e as Map<String, dynamic>)).toList();
}

/// Retourne l'exoplanète du jour à partir d'une liste déjà chargée.
/// Avance d'une planète par jour depuis le 1er janvier 2026.
Exoplanet dailyExoplanet(List<Exoplanet> planets) {
  final origin = DateTime(2026, 1, 1);
  final today  = DateTime.now();
  final dayIndex = today.difference(origin).inDays.abs();
  return planets[dayIndex % planets.length];
}
