import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MountainData {
  final String name, country, range, famousFor;
  final int elevation;
  final String? imageUrl, firstAscent;

  String? get noImageMessage => imageUrl != null ? null : '🏔️ No image available for this mountain';

  const MountainData({
    required this.name, required this.country, required this.range,
    required this.elevation, required this.famousFor, this.imageUrl, this.firstAscent,
  });

  factory MountainData.fromJson(Map<String, dynamic> j) => MountainData(
    name:        j['n']  ?? '',
    country:     j['co'] ?? '',
    range:       j['ra'] ?? '',
    elevation:   (j['el'] as num?)?.toInt() ?? 0,
    famousFor:   j['fa'] ?? '',
    imageUrl:    j['im'] as String?,
    firstAscent: j['fc'] as String?,
  );
}

Future<List<MountainData>> loadMountains() async {
  final raw = await rootBundle.loadString('assets/world/mountains.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MountainData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MountainData>? _shuffledCache;

MountainData dailyMountain(List<MountainData> mountains) {
  if (_shuffledCache == null) {
    final list = List<MountainData>.from(mountains);
    final rng = math.Random(20260601);
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
