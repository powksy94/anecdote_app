import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, inv=best-known invention(s), cc=ISO2 country code(s) ("/"-joined when several),
// yr=lifespan (null if undocumented), fa=fact, im=imageUrl

class LegendaryInventorData {
  final String name, invention, countryCode, fact;
  final String? years;
  final String? imageUrl;

  const LegendaryInventorData({
    required this.name, required this.invention, required this.countryCode, required this.fact,
    this.years, this.imageUrl,
  });

  factory LegendaryInventorData.fromJson(Map<String, dynamic> j) => LegendaryInventorData(
    name:        j['n']   as String,
    invention:   j['inv'] as String,
    countryCode: j['cc']  as String,
    fact:        j['fa']  as String,
    years:       j['yr']  as String?,
    imageUrl:    (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<LegendaryInventorData>> loadLegendaryInventors() async {
  final raw = await rootBundle.loadString('assets/tech/legendary_inventors.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => LegendaryInventorData.fromJson(e as Map<String, dynamic>)).toList();
}

List<LegendaryInventorData>? _shuffledCache;

LegendaryInventorData dailyLegendaryInventor(List<LegendaryInventorData> items) {
  if (_shuffledCache == null) {
    final list = List<LegendaryInventorData>.from(items);
    final rng = math.Random(20261123);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 11, 23);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
