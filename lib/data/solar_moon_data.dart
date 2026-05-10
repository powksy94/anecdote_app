import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class SolarMoonData {
  final String name, planet, discoverer, features;
  final int diameter, discoveryYear;
  final double orbitalPeriod;

  const SolarMoonData({
    required this.name, required this.planet,
    required this.discoverer, required this.features,
    required this.diameter, required this.discoveryYear,
    required this.orbitalPeriod,
  });

  factory SolarMoonData.fromJson(Map<String, dynamic> j) => SolarMoonData(
    name:          j['n']  ?? '',
    planet:        j['pl'] ?? '',
    diameter:      (j['di'] as num?)?.toInt() ?? 0,
    orbitalPeriod: (j['op'] as num?)?.toDouble() ?? 0,
    discoveryYear: (j['dy'] as num?)?.toInt() ?? 0,
    discoverer:    j['dc'] ?? '',
    features:      j['fe'] ?? '',
  );
}

Future<List<SolarMoonData>> loadSolarMoons() async {
  final raw = await rootBundle.loadString('assets/solar_moons.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SolarMoonData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SolarMoonData>? _shuffledCache;

SolarMoonData dailySolarMoon(List<SolarMoonData> moons) {
  if (_shuffledCache == null) {
    final list = List<SolarMoonData>.from(moons);
    final rng = math.Random(20260105);
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
