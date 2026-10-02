import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class OttomanSultanData {
  final String name, era, famousFor;
  final String? nickname, imageUrl, historicalNote;
  final int reignStart, reignEnd;

  const OttomanSultanData({
    required this.name, required this.era, required this.famousFor,
    required this.reignStart, required this.reignEnd, this.nickname, this.imageUrl,
    this.historicalNote,
  });

  String? get noImageMessage => imageUrl != null ? null : '👑 No portrait available for this sultan';

  factory OttomanSultanData.fromJson(Map<String, dynamic> j) => OttomanSultanData(
    name:        j['n']  ?? '',
    era:         j['dy'] ?? '',
    reignStart:  (j['rs'] as num?)?.toInt() ?? 0,
    reignEnd:    (j['re'] as num?)?.toInt() ?? 0,
    nickname:    j['ni'] as String?,
    famousFor:   j['fa'] ?? '',
    imageUrl:    j['im'] as String?,
    historicalNote: j['hn'] as String?,
  );
}

Future<List<OttomanSultanData>> loadOttomanSultans() async {
  final raw = await rootBundle.loadString('assets/history/ottoman_empire.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => OttomanSultanData.fromJson(e as Map<String, dynamic>)).toList();
}

List<OttomanSultanData>? _shuffledCache;

OttomanSultanData dailyOttomanSultan(List<OttomanSultanData> sultans) {
  if (_shuffledCache == null) {
    final list = List<OttomanSultanData>.from(sultans);
    final rng = math.Random(20261002);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 10, 2);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
