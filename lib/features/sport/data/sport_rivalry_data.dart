import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=rivalry title ("X vs Y"), sp=sport, cc=ISO2 country code(s), "/"-joined for dual
// nationality, yr=years the rivalry was active, ctx=context, fa=fact/highlight
//
// Text-only category (no image field): ImageContentCard only supports a single portrait,
// which doesn't fit a two-person duel, so this falls back to the standard icon-based
// ContentCard automatically (selectContentCard picks it whenever imageUrl is null).

class SportRivalryData {
  final String name, sport, years, context, fact;
  final String? countryCode;

  const SportRivalryData({
    required this.name, required this.sport, required this.years,
    required this.context, required this.fact,
    this.countryCode,
  });

  factory SportRivalryData.fromJson(Map<String, dynamic> j) => SportRivalryData(
    name:        j['n']   as String,
    sport:       j['sp']  as String,
    years:       j['yr']  as String,
    context:     j['ctx'] as String,
    fact:        j['fa']  as String,
    countryCode: j['cc'] as String?,
  );
}

Future<List<SportRivalryData>> loadSportRivalries() async {
  final raw = await rootBundle.loadString('assets/sport/sport_rivalries.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SportRivalryData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SportRivalryData>? _shuffledCache;

SportRivalryData dailySportRivalry(List<SportRivalryData> items) {
  if (_shuffledCache == null) {
    final list = List<SportRivalryData>.from(items);
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
