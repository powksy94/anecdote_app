import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, inv=invention, cc=ISO2 country code(s) ("/"-joined when several),
// yr=lifespan (null if undocumented), ctx=era context (null if no reliable documented
// context exists), fa=fact, im=imageUrl

class WomanInventorData {
  final String name, invention, countryCode, fact;
  final String? years;
  final String? context;
  final String? imageUrl;

  const WomanInventorData({
    required this.name, required this.invention, required this.countryCode, required this.fact,
    this.years, this.context, this.imageUrl,
  });

  factory WomanInventorData.fromJson(Map<String, dynamic> j) => WomanInventorData(
    name:        j['n']   as String,
    invention:   j['inv'] as String,
    countryCode: j['cc']  as String,
    fact:        j['fa']  as String,
    years:       j['yr']  as String?,
    context:     j['ctx'] as String?,
    imageUrl:    (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<WomanInventorData>> loadWomanInventors() async {
  final raw = await rootBundle.loadString('assets/tech/women_inventors.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => WomanInventorData.fromJson(e as Map<String, dynamic>)).toList();
}

List<WomanInventorData>? _shuffledCache;

WomanInventorData dailyWomanInventor(List<WomanInventorData> items) {
  if (_shuffledCache == null) {
    final list = List<WomanInventorData>.from(items);
    final rng = math.Random(20261031);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 10, 31);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
