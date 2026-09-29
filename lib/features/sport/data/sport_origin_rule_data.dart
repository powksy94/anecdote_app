import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=title/hook, sp=sport, cc=ISO2 country code, yr=year or era, fa=fact
//
// Text-only category (no image field): this content is about sports and their rules,
// not about a single person, so it falls back to the standard icon-based ContentCard
// automatically (selectContentCard picks it whenever imageUrl is null).

class SportOriginRuleData {
  final String title, sport, year, fact;
  final String? countryCode;

  const SportOriginRuleData({
    required this.title, required this.sport, required this.year, required this.fact,
    this.countryCode,
  });

  factory SportOriginRuleData.fromJson(Map<String, dynamic> j) => SportOriginRuleData(
    title:       j['n']   as String,
    sport:       j['sp']  as String,
    year:        j['yr']  as String,
    fact:        j['fa']  as String,
    countryCode: j['cc'] as String?,
  );
}

Future<List<SportOriginRuleData>> loadSportOriginRules() async {
  final raw = await rootBundle.loadString('assets/sport/sport_origins_rules.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SportOriginRuleData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SportOriginRuleData>? _shuffledCache;

SportOriginRuleData dailySportOriginRule(List<SportOriginRuleData> items) {
  if (_shuffledCache == null) {
    final list = List<SportOriginRuleData>.from(items);
    final rng = math.Random(20260929);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 9, 29);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
