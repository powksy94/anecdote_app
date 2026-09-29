import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, sp=sport, cc=ISO2 country code, yr=lifespan (birth-death), ctx=era/social context,
// fa=achievement/impact, im=imageUrl

class SportGreatWomanData {
  final String name, sport, years, context, achievement;
  final String? countryCode;
  final String? imageUrl;

  const SportGreatWomanData({
    required this.name, required this.sport, required this.years,
    required this.context, required this.achievement,
    this.countryCode, this.imageUrl,
  });

  factory SportGreatWomanData.fromJson(Map<String, dynamic> j) => SportGreatWomanData(
    name:        j['n']   as String,
    sport:       j['sp']  as String,
    years:       j['yr']  as String,
    context:     j['ctx'] as String,
    achievement: j['fa']  as String,
    countryCode: j['cc'] as String?,
    imageUrl:    (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<SportGreatWomanData>> loadSportGreatWomen() async {
  final raw = await rootBundle.loadString('assets/sport/sport_great_women.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SportGreatWomanData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SportGreatWomanData>? _shuffledCache;

SportGreatWomanData dailySportGreatWoman(List<SportGreatWomanData> items) {
  if (_shuffledCache == null) {
    final list = List<SportGreatWomanData>.from(items);
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
