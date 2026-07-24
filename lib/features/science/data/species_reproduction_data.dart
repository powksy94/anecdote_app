import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class SpeciesReproductionData {
  final String name, strategy, type, gestation, fact;

  const SpeciesReproductionData({
    required this.name, required this.strategy, required this.type,
    required this.gestation, required this.fact,
  });

  factory SpeciesReproductionData.fromJson(Map<String, dynamic> j) => SpeciesReproductionData(
    name:      j['n']    ?? '',
    strategy:  j['strat'] ?? '',
    type:      j['typ']  ?? '',
    gestation: j['gest'] ?? '',
    fact:      j['fa']   ?? '',
  );
}

Future<List<SpeciesReproductionData>> loadSpeciesReproduction() async {
  final raw = await rootBundle.loadString('assets/science/species_reproduction.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SpeciesReproductionData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SpeciesReproductionData>? _shuffledCache;

SpeciesReproductionData dailySpeciesReproduction(List<SpeciesReproductionData> species) {
  if (_shuffledCache == null) {
    final list = List<SpeciesReproductionData>.from(species);
    final rng = math.Random(20260501);
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
