import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class PacificIslandData {
  final String name, archipelago, territory, country, ocean;
  final double? area;
  final int? population;

  const PacificIslandData({
    required this.name, required this.archipelago,
    required this.territory, required this.country, required this.ocean,
    this.area, this.population,
  });

  factory PacificIslandData.fromJson(Map<String, dynamic> j) => PacificIslandData(
    name:         j['n']        ?? '', 
    archipelago:  j['ar']       ?? '', 
    territory:    j['te']       ?? '', 
    country:      j['co']       ?? '', 
    ocean:        j['oc']       ?? '',
    area:         (j['ar_km2'] as num?)?.toDouble(),
    population:   (j['po']      as num?)?.toInt(),
  );
}

Future<List<PacificIslandData>> loadPacificIslands() async{
  final raw = await rootBundle.loadString('assets/pacific_islands.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => PacificIslandData.fromJson(e as Map<String, dynamic>)).toList();
}

List<PacificIslandData>? _shuffledCache;

PacificIslandData dailyPacificIsland(List<PacificIslandData> islands) {
  if (_shuffledCache == null) {
    final list = List<PacificIslandData>.from(islands);
    final rng = math.Random(20260103);
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