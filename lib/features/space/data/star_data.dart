import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class StarData {
  final String name, constellation, category, system, galaxy;
  final double distance, magnitude;
  final double? radius, mass;
  final int planets;
  final String? imageUrl;

  const StarData({
    required this.name, required this.constellation,
    required this.category, required this.system, required this.galaxy,
    required this.distance, required this.magnitude,
    required this.planets,
    this.radius, this.mass,
    this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null
      ? null
      : '⭐ $name ($category) — no telescope image currently available';

  factory StarData.fromJson(Map<String, dynamic> j) => StarData(
    name:          j['n']  ?? '',
    constellation: j['co'] ?? '',
    distance:      (j['di'] as num?)?.toDouble() ?? 0,
    magnitude:     (j['ma'] as num?)?.toDouble() ?? 0,
    category:      j['ca'] ?? '',
    system:        j['sy'] ?? '',
    galaxy:        j['ga'] ?? '',
    planets:       (j['pl'] as num?)?.toInt() ?? 0,
    radius:        (j['ra'] as num?)?.toDouble(),
    mass:          (j['ms'] as num?)?.toDouble(),
    imageUrl:      (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<StarData>> loadStars() async {
  final raw = await rootBundle.loadString('assets/space/stars.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => StarData.fromJson(e as Map<String, dynamic>)).toList();
}

List<StarData>? _shuffledCache;

StarData dailyStar(List<StarData> stars) {
  if (_shuffledCache == null) {
    final list = List<StarData>.from(stars);
    final rng = math.Random(20260104);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 1, 1);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
