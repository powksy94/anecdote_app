import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class EgyptianMythologyData {
  final String name, domain, symbol, famousFor;
  final String? imageUrl;

  const EgyptianMythologyData({
    required this.name, required this.domain, required this.symbol,
    required this.famousFor, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '𓂀 No image available for this figure';

  factory EgyptianMythologyData.fromJson(Map<String, dynamic> j) => EgyptianMythologyData(
    name:       j['n']   ?? '',
    domain:     j['dom'] ?? '',
    symbol:     j['sym'] ?? '',
    famousFor:  j['fa']  ?? '',
    imageUrl:   j['im'] as String?,
  );
}

Future<List<EgyptianMythologyData>> loadEgyptianMythology() async {
  final raw = await rootBundle.loadString('assets/mythology/egyptian_mythology.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => EgyptianMythologyData.fromJson(e as Map<String, dynamic>)).toList();
}

List<EgyptianMythologyData>? _shuffledCache;

EgyptianMythologyData dailyEgyptianMythology(List<EgyptianMythologyData> figures) {
  if (_shuffledCache == null) {
    final list = List<EgyptianMythologyData>.from(figures);
    final rng = math.Random(20260303);
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
