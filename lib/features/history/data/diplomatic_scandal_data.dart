import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=title/hook, cc=ISO2 country code(s), yr=year or range, ctx=political/geopolitical
// context, fa=fact
//
// Text-only category (no image field): this content is about diplomatic incidents
// between nations, not about a single person's portrait, so it falls back to the
// standard icon-based ContentCard automatically (selectContentCard picks it whenever
// imageUrl is null).

class DiplomaticScandalData {
  final String title, year, context, fact;
  final String? countryCode;

  const DiplomaticScandalData({
    required this.title, required this.year, required this.context, required this.fact,
    this.countryCode,
  });

  factory DiplomaticScandalData.fromJson(Map<String, dynamic> j) => DiplomaticScandalData(
    title:       j['n']   as String,
    year:        j['yr']  as String,
    context:     j['ctx'] as String,
    fact:        j['fa']  as String,
    countryCode: j['cc'] as String?,
  );
}

Future<List<DiplomaticScandalData>> loadDiplomaticScandals() async {
  final raw = await rootBundle.loadString('assets/history/diplomatic_scandals.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => DiplomaticScandalData.fromJson(e as Map<String, dynamic>)).toList();
}

List<DiplomaticScandalData>? _shuffledCache;

DiplomaticScandalData dailyDiplomaticScandal(List<DiplomaticScandalData> items) {
  if (_shuffledCache == null) {
    final list = List<DiplomaticScandalData>.from(items);
    final rng = math.Random(20260930);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 9, 30);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
