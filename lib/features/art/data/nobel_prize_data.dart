import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, yr=year, ca=category, co=country, fa=famous_for, im=imageUrl, wl=warningLevel, wi=warningText

class NobelPrizeData {
  final String name, year, category, country, famousFor;
  final String? imageUrl;
  final String? warningLevel;
  final String? warningText;

  const NobelPrizeData({
    required this.name, required this.year, required this.category,
    required this.country, required this.famousFor,
    this.imageUrl, this.warningLevel, this.warningText,
  });

  factory NobelPrizeData.fromJson(Map<String, dynamic> j) => NobelPrizeData(
    name:         j['n']  ?? '',
    year:         j['yr'] ?? '',
    category:     j['ca'] ?? '',
    country:      j['co'] ?? '',
    famousFor:    j['fa'] ?? '',
    imageUrl:     j['im'] as String?,
    warningLevel: j['wl'] as String?,
    warningText:  j['wi'] as String?,
  );

  String? get noImageMessage {
    if (imageUrl != null) return null;
    return '🏆 No image available for this laureate';
  }
}

Future<List<NobelPrizeData>> loadNobelPrizes() async {
  final raw = await rootBundle.loadString('assets/art/nobel_prize.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => NobelPrizeData.fromJson(e as Map<String, dynamic>)).toList();
}

List<NobelPrizeData>? _shuffledCache;

NobelPrizeData dailyNobelPrize(List<NobelPrizeData> laureates) {
  if (_shuffledCache == null) {
    final list = List<NobelPrizeData>.from(laureates);
    final rng = math.Random(20260206);
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
