import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class BritishMonarchData {
  final String name, dynasty, famousFor;
  final String? nickname, imageUrl, historicalNote;
  final int reignStart;
  final int? reignEnd;

  const BritishMonarchData({
    required this.name, required this.dynasty, required this.famousFor,
    required this.reignStart, this.reignEnd, this.nickname, this.imageUrl,
    this.historicalNote,
  });

  String? get noImageMessage => imageUrl != null ? null : '👑 No portrait available for this monarch';

  factory BritishMonarchData.fromJson(Map<String, dynamic> j) => BritishMonarchData(
    name:        j['n']  ?? '',
    dynasty:     j['dy'] ?? '',
    reignStart:  (j['rs'] as num?)?.toInt() ?? 0,
    reignEnd:    (j['re'] as num?)?.toInt(),
    nickname:    j['ni'] as String?,
    famousFor:   j['fa'] ?? '',
    imageUrl:    j['im'] as String?,
    historicalNote: j['hn'] as String?,
  );
}

Future<List<BritishMonarchData>> loadBritishMonarchs() async {
  final raw = await rootBundle.loadString('assets/history/british_monarchy.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => BritishMonarchData.fromJson(e as Map<String, dynamic>)).toList();
}

List<BritishMonarchData>? _shuffledCache;

BritishMonarchData dailyBritishMonarch(List<BritishMonarchData> monarchs) {
  if (_shuffledCache == null) {
    final list = List<BritishMonarchData>.from(monarchs);
    final rng = math.Random(20261001);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 10, 1);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
