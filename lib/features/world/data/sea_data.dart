import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class SeaData {
  final String name, location, ocean, famousFor;
  final int area;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '🌊 No image available for this sea';

  const SeaData({
    required this.name, required this.location, required this.ocean,
    required this.area, required this.famousFor, this.imageUrl,
  });

  factory SeaData.fromJson(Map<String, dynamic> j) => SeaData(
    name:      j['n']  ?? '',
    location:  j['lo'] ?? '',
    ocean:     j['oc'] ?? '',
    area:      (j['ar'] as num?)?.toInt() ?? 0,
    famousFor: j['fa'] ?? '',
    imageUrl:  j['im'] as String?,
  );
}

Future<List<SeaData>> loadSeas() async {
  final raw = await rootBundle.loadString('assets/world/seas.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SeaData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SeaData>? _shuffledCache;

SeaData dailySea(List<SeaData> seas) {
  if (_shuffledCache == null) {
    final list = List<SeaData>.from(seas);
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
