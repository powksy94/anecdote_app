import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, bi=birthYear, na=nationality, sp=specialty, ach=achievements,
// im=imageUrl, nim=noImageMessage, wl=warningLevel, wi=warningText

class GamingLegendData {
  final String name, nationality, specialty, achievements;
  final int birthYear;
  final String? imageUrl;
  final String? noImageMessage;
  final String? warningLevel;
  final String? warningText;

  const GamingLegendData({
    required this.name, required this.birthYear, required this.nationality,
    required this.specialty, required this.achievements,
    this.imageUrl, this.noImageMessage, this.warningLevel, this.warningText,
  });

  factory GamingLegendData.fromJson(Map<String, dynamic> j) => GamingLegendData(
    name:           j['n']   ?? '',
    birthYear:      (j['bi'] as num).toInt(),
    nationality:    j['na']  ?? '',
    specialty:      j['sp']  ?? '',
    achievements:   j['ach'] ?? '',
    imageUrl:       j['im']  as String?,
    noImageMessage: j['nim'] as String?,
    warningLevel:   j['wl']  as String?,
    warningText:    j['wi']  as String?,
  );
}

Future<List<GamingLegendData>> loadGamingLegends() async {
  final raw = await rootBundle.loadString('assets/gaming/gaming_legends.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => GamingLegendData.fromJson(e as Map<String, dynamic>)).toList();
}

List<GamingLegendData>? _shuffledCache;

GamingLegendData dailyGamingLegend(List<GamingLegendData> items) {
  if (_shuffledCache == null) {
    final list = List<GamingLegendData>.from(items);
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
