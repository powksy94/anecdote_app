import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class DesertData {
  final String name, country, type, famousFor;
  final int area;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '🏜️ No image available for this desert';

  const DesertData({
    required this.name, required this.country, required this.type,
    required this.area, required this.famousFor, this.imageUrl,
  });

  factory DesertData.fromJson(Map<String, dynamic> j) => DesertData(
    name:      j['n']  ?? '',
    country:   j['co'] ?? '',
    type:      j['ty'] ?? '',
    area:      (j['ar'] as num?)?.toInt() ?? 0,
    famousFor: j['fa'] ?? '',
    imageUrl:  j['im'] as String?,
  );
}

Future<List<DesertData>> loadDeserts() async {
  final raw = await rootBundle.loadString('assets/world/deserts.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => DesertData.fromJson(e as Map<String, dynamic>)).toList();
}

List<DesertData>? _shuffledCache;

DesertData dailyDesert(List<DesertData> deserts) {
  if (_shuffledCache == null) {
    final list = List<DesertData>.from(deserts);
    final rng = math.Random(20260301);
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
