import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=record name, sp=sport, hd=holder (person, duo or team; null if no single holder),
// cc=ISO2 country code(s) for flag rendering ("/"-joined for dual nationality, null if
// team/no single nationality applies), yr=year, fa=fact/context, im=imageUrl

class SportRecordData {
  final String name, sport, year, fact;
  final String? holder;
  final String? countryCode;
  final String? imageUrl;

  const SportRecordData({
    required this.name, required this.sport, required this.year, required this.fact,
    this.holder, this.countryCode, this.imageUrl,
  });

  factory SportRecordData.fromJson(Map<String, dynamic> j) => SportRecordData(
    name:        j['n']  as String,
    sport:       j['sp'] as String,
    year:        j['yr'] as String,
    fact:        j['fa'] as String,
    holder:      j['hd'] as String?,
    countryCode: j['cc'] as String?,
    imageUrl:    (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<SportRecordData>> loadSportRecords() async {
  final raw = await rootBundle.loadString('assets/sport/sport_records.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SportRecordData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SportRecordData>? _shuffledCache;

SportRecordData dailySportRecord(List<SportRecordData> items) {
  if (_shuffledCache == null) {
    final list = List<SportRecordData>.from(items);
    final rng = math.Random(20260928);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 9, 28);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
