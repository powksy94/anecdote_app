import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class InstrumentData {
  final String name, family, era, fact;
  final String? imageUrl;

  const InstrumentData({
    required this.name, required this.family, required this.era,
    required this.fact, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '🎼 No image available for this instrument';

  factory InstrumentData.fromJson(Map<String, dynamic> j) => InstrumentData(
    name:      j['n']   ?? '',
    family:    j['fam'] ?? '',
    era:       j['ep']  ?? '',
    fact:      j['fa']  ?? '',
    imageUrl:  j['im'] as String?,
  );
}

Future<List<InstrumentData>> loadInstruments() async {
  final raw = await rootBundle.loadString('assets/music/instruments.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => InstrumentData.fromJson(e as Map<String, dynamic>)).toList();
}

List<InstrumentData>? _shuffledCache;

InstrumentData dailyInstrument(List<InstrumentData> instruments) {
  if (_shuffledCache == null) {
    final list = List<InstrumentData>.from(instruments);
    final rng = math.Random(20260203);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 1, 1);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
