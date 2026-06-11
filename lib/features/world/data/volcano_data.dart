import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class VolcanoData {
  final String name, country, type, status, lastEruption, location, famousFor;
  final int? elevation;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '🌋 No imagery available for this volcano';

  const VolcanoData({
    required this.name, required this.country, required this.type,
    required this.status, required this.lastEruption, required this.location,
    required this.famousFor, this.elevation, this.imageUrl,
  });

  factory VolcanoData.fromJson(Map<String, dynamic> j) => VolcanoData(
    name:         j['n']  ?? '',
    country:      j['co'] ?? '',
    type:         j['ty'] ?? '',
    status:       j['st'] ?? '',
    elevation:    (j['el'] as num?)?.toInt(),
    lastEruption: j['le']?.toString() ?? '',
    location:     j['lo'] ?? '',
    famousFor:    j['fa'] ?? '',
    imageUrl:     j['im'] as String?,
  );
}

Future<List<VolcanoData>> loadVolcanoes() async {
  final raw = await rootBundle.loadString('assets/science/volcanoes.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => VolcanoData.fromJson(e as Map<String, dynamic>)).toList();
}

List<VolcanoData>? _shuffledCache;

VolcanoData dailyVolcano(List<VolcanoData> volcanoes) {
  if (_shuffledCache == null) {
    final list = List<VolcanoData>.from(volcanoes);
    final rng = math.Random(20260202);
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
