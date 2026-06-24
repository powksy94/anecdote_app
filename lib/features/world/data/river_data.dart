import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class RiverData {
  final String name, country, mouth, famousFor;
  final int length;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '🏞️ No image available for this river';

  const RiverData({
    required this.name, required this.country, required this.mouth,
    required this.length, required this.famousFor, this.imageUrl,
  });

  factory RiverData.fromJson(Map<String, dynamic> j) => RiverData(
    name:      j['n']  ?? '',
    country:   j['co'] ?? '',
    mouth:     j['mo'] ?? '',
    length:    (j['le'] as num?)?.toInt() ?? 0,
    famousFor: j['fa'] ?? '',
    imageUrl:  j['im'] as String?,
  );
}

Future<List<RiverData>> loadRivers() async {
  final raw = await rootBundle.loadString('assets/world/rivers.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => RiverData.fromJson(e as Map<String, dynamic>)).toList();
}

List<RiverData>? _shuffledCache;

RiverData dailyRiver(List<RiverData> rivers) {
  if (_shuffledCache == null) {
    final list = List<RiverData>.from(rivers);
    final rng = math.Random(20260302);
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
