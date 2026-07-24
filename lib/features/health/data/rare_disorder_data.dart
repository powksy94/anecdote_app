import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class RareDisorderData {
  final String name, fact, discovered, prevalence, heredity, dailyLifeImpact;

  const RareDisorderData({
    required this.name, required this.fact, required this.discovered,
    required this.prevalence, required this.heredity, required this.dailyLifeImpact,
  });

  factory RareDisorderData.fromJson(Map<String, dynamic> j) => RareDisorderData(
    name:            j['n']   ?? '',
    fact:            j['fa']  ?? '',
    discovered:      j['ds']  ?? '',
    prevalence:      j['pr']  ?? '',
    heredity:        j['her'] ?? '',
    dailyLifeImpact: j['dl']  ?? '',
  );
}

Future<List<RareDisorderData>> loadRareDisorders() async {
  final raw = await rootBundle.loadString('assets/health/rare_disorders.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => RareDisorderData.fromJson(e as Map<String, dynamic>)).toList();
}

List<RareDisorderData>? _shuffledCache;

RareDisorderData dailyRareDisorder(List<RareDisorderData> disorders) {
  if (_shuffledCache == null) {
    final list = List<RareDisorderData>.from(disorders);
    final rng = math.Random(20260402);
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
