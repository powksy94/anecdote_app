import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class BattleData {
  final String name, date, location, belligerents, result, famousFor;
  final String? imageUrl;

  const BattleData({
    required this.name, required this.date, required this.location,
    required this.belligerents, required this.result, required this.famousFor,
    this.imageUrl,
  });

  factory BattleData.fromJson(Map<String, dynamic> j) => BattleData(
    name:         j['n']  ?? '',
    date:         j['da'] ?? '',
    location:     j['lo'] ?? '',
    belligerents: j['be'] ?? '',
    result:       j['re'] ?? '',
    famousFor:    j['fa'] ?? '',
    imageUrl:     j['im'] as String?,
  );

  String? get noImageMessage {
    if (imageUrl != null) return null;
    final year = int.tryParse(date.replaceAll(RegExp(r'[^0-9\-]'), '').split('-').first);
    if (year != null && year < 0) return '📜 No visual records survive from antiquity';
    if (year != null && year < 1000) return '📜 No contemporary imagery survives from this period';
    if (year != null && year < 1400) return '🏰 No visual records from the medieval period';
    return '🖼️ No image available for this battle';
  }
}

Future<List<BattleData>> loadBattles() async {
  final raw = await rootBundle.loadString('assets/history/battles.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => BattleData.fromJson(e as Map<String, dynamic>)).toList();
}

List<BattleData>? _shuffledCache;

BattleData dailyBattle(List<BattleData> battles) {
  if (_shuffledCache == null) {
    final list = List<BattleData>.from(battles);
    final rng = math.Random(20260113);
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
