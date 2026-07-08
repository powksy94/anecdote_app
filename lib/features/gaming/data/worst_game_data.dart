import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class WorstGameData {
  final String name, publisher, reason;
  final int year;
  final int? score;
  final String? imageUrl;
  final String? noImageMessage;

  const WorstGameData({
    required this.name, required this.year, required this.publisher,
    required this.reason, this.score,
    this.imageUrl, this.noImageMessage,
  });

  factory WorstGameData.fromJson(Map<String, dynamic> j) => WorstGameData(
    name:           j['n']   ?? '',
    year:           (j['y'] as num).toInt(),
    publisher:      j['pu']  ?? '',
    reason:         j['rea'] ?? '',
    score:          j['sc']  != null ? (j['sc'] as num).toInt() : null,
    imageUrl:       j['im']  as String?,
    noImageMessage: j['nim'] as String?,
  );
}

Future<List<WorstGameData>> loadWorstGames() async {
  final raw = await rootBundle.loadString('assets/gaming/worst_games.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => WorstGameData.fromJson(e as Map<String, dynamic>)).toList();
}

List<WorstGameData>? _shuffledCache;

WorstGameData dailyWorstGame(List<WorstGameData> items) {
  if (_shuffledCache == null) {
    final list = List<WorstGameData>.from(items);
    final rng = math.Random(20260204);
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