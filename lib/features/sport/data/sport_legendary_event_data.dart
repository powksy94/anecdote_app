import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=event title, sp=sport, pr=protagonist (person; null if team-collective moment with
// no single figure), cc=ISO2 country code (null if no single nationality applies),
// yr=year, fa=fact/highlight, im=imageUrl

class SportLegendaryEventData {
  final String name, sport, year, fact;
  final String? protagonist;
  final String? countryCode;
  final String? imageUrl;

  const SportLegendaryEventData({
    required this.name, required this.sport, required this.year, required this.fact,
    this.protagonist, this.countryCode, this.imageUrl,
  });

  factory SportLegendaryEventData.fromJson(Map<String, dynamic> j) => SportLegendaryEventData(
    name:         j['n']  as String,
    sport:        j['sp'] as String,
    year:         j['yr'] as String,
    fact:         j['fa'] as String,
    protagonist:  j['pr'] as String?,
    countryCode:  j['cc'] as String?,
    imageUrl:     (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<SportLegendaryEventData>> loadSportLegendaryEvents() async {
  final raw = await rootBundle.loadString('assets/sport/sport_legendary_events.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SportLegendaryEventData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SportLegendaryEventData>? _shuffledCache;

SportLegendaryEventData dailySportLegendaryEvent(List<SportLegendaryEventData> items) {
  if (_shuffledCache == null) {
    final list = List<SportLegendaryEventData>.from(items);
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
