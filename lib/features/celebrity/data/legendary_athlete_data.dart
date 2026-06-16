import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, co=country, sp=sport, yr=active years, tr=trophies (nullable), md=medals (nullable), fa=impact, im=imageUrl

class LegendaryAthleteData {
  final String name, country, sport, activeYears, impact;
  final String? trophies;
  final String? medals;
  final String? imageUrl;

  const LegendaryAthleteData({
    required this.name, required this.country, required this.sport,
    required this.activeYears, required this.impact,
    this.trophies, this.medals, this.imageUrl,
  });

  factory LegendaryAthleteData.fromJson(Map<String, dynamic> j) => LegendaryAthleteData(
    name:        j['n']  as String,
    country:     j['co'] as String,
    sport:       j['sp'] as String,
    activeYears: j['yr'] as String,
    trophies:    j['tr'] as String?,
    medals:      j['md'] as String?,
    impact:      j['fa'] as String,
    imageUrl:    (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<LegendaryAthleteData>> loadLegendaryAthletes() async {
  final raw = await rootBundle.loadString('assets/celebrity/legendary_athletes.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => LegendaryAthleteData.fromJson(e as Map<String, dynamic>)).toList();
}

List<LegendaryAthleteData>? _shuffledCache;

LegendaryAthleteData dailyLegendaryAthlete(List<LegendaryAthleteData> items) {
  if (_shuffledCache == null) {
    final list = List<LegendaryAthleteData>.from(items);
    final rng = math.Random(20260618);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 6, 18);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
