import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, co=country, yr=years, fi=field, ctx=socio-feminist context, fa=impact, im=imageUrl

class PioneerWomanData {
  final String name, country, years, field, context, impact;
  final String? imageUrl;

  const PioneerWomanData({
    required this.name, required this.country, required this.years,
    required this.field, required this.context, required this.impact,
    this.imageUrl,
  });

  factory PioneerWomanData.fromJson(Map<String, dynamic> j) => PioneerWomanData(
    name:    j['n']   as String,
    country: j['co']  as String,
    years:   j['yr']  as String,
    field:   j['fi']  as String,
    context: j['ctx'] as String,
    impact:  j['fa']  as String,
    imageUrl: (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<PioneerWomanData>> loadPioneerWomen() async {
  final raw = await rootBundle.loadString('assets/celebrity/pioneer_women.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => PioneerWomanData.fromJson(e as Map<String, dynamic>)).toList();
}

List<PioneerWomanData>? _shuffledCache;

PioneerWomanData dailyPioneerWoman(List<PioneerWomanData> items) {
  if (_shuffledCache == null) {
    final list = List<PioneerWomanData>.from(items);
    final rng = math.Random(20260617);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 6, 17);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
