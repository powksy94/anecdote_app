import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class CommonHealthFactData {
  final String title, fact;

  const CommonHealthFactData({required this.title, required this.fact});

  factory CommonHealthFactData.fromJson(Map<String, dynamic> j) => CommonHealthFactData(
    title: j['n']  ?? '',
    fact:  j['fa'] ?? '',
  );
}

Future<List<CommonHealthFactData>> loadCommonHealthFacts() async {
  final raw = await rootBundle.loadString('assets/health/common_health_facts.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => CommonHealthFactData.fromJson(e as Map<String, dynamic>)).toList();
}

List<CommonHealthFactData>? _shuffledCache;

CommonHealthFactData dailyCommonHealthFact(List<CommonHealthFactData> facts) {
  if (_shuffledCache == null) {
    final list = List<CommonHealthFactData>.from(facts);
    final rng = math.Random(20260403);
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
