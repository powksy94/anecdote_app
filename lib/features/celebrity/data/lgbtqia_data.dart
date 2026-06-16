import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, co=country, yr=years, or=orientation (null if uncertain), fi=field, fa=impact, im=imageUrl

class LgbtqiaData {
  final String name, country, years, field, impact;
  final String? orientation;
  final String? imageUrl;

  const LgbtqiaData({
    required this.name, required this.country, required this.years,
    required this.field, required this.impact,
    this.orientation, this.imageUrl,
  });

  factory LgbtqiaData.fromJson(Map<String, dynamic> j) => LgbtqiaData(
    name:        j['n']  as String,
    country:     j['co'] as String,
    years:       j['yr'] as String,
    orientation: j['or'] as String?,
    field:       j['fi'] as String,
    impact:      j['fa'] as String,
    imageUrl:    (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );

  bool get isOrientationUncertain => orientation == null;
}

Future<List<LgbtqiaData>> loadLgbtqiaPersonalities() async {
  final raw = await rootBundle.loadString('assets/celebrity/lgbtqia.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => LgbtqiaData.fromJson(e as Map<String, dynamic>)).toList();
}

List<LgbtqiaData>? _shuffledCache;

LgbtqiaData dailyLgbtqia(List<LgbtqiaData> items) {
  if (_shuffledCache == null) {
    final list = List<LgbtqiaData>.from(items);
    final rng = math.Random(20260616);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 6, 16);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
