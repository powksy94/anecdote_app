import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class KingOfFranceData {
  final String name, dynasty, famousFor;
  final String? nickname;
  final int reignStart, reignEnd;

  const KingOfFranceData({
    required this.name, required this.dynasty, required this.famousFor,
    required this.reignStart, required this.reignEnd, this.nickname,
  });

  factory KingOfFranceData.fromJson(Map<String, dynamic> j) => KingOfFranceData(
    name:        j['n']  ?? '',
    dynasty:     j['dy'] ?? '',
    reignStart:  (j['rs'] as num?)?.toInt() ?? 0,
    reignEnd:    (j['re'] as num?)?.toInt() ?? 0,
    nickname:    j['ni'] as String?,
    famousFor:   j['fa'] ?? '',
  );
}

Future<List<KingOfFranceData>> loadKingsOfFrance() async {
  final raw = await rootBundle.loadString('assets/history/kings_of_france.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => KingOfFranceData.fromJson(e as Map<String, dynamic>)).toList();
}

List<KingOfFranceData>? _shuffledCache;

KingOfFranceData dailyKingOfFrance(List<KingOfFranceData> kings) {
  if (_shuffledCache == null) {
    final list = List<KingOfFranceData>.from(kings);
    final rng = math.Random(20260106);
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
