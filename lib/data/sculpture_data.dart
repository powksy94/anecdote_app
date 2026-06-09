import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, ar=artist, yr=year, ma=material, lo=location, st=style, fa=famous_for, im=imageUrl

class SculptureData {
  final String name, artist, year, material, location, style, famousFor;
  final String? imageUrl;

  const SculptureData({
    required this.name, required this.artist, required this.year,
    required this.material, required this.location, required this.style,
    required this.famousFor, this.imageUrl,
  });

  factory SculptureData.fromJson(Map<String, dynamic> j) => SculptureData(
    name:      j['n']  ?? '',
    artist:    j['ar'] ?? '',
    year:      j['yr'] ?? '',
    material:  j['ma'] ?? '',
    location:  j['lo'] ?? '',
    style:     j['st'] ?? '',
    famousFor: j['fa'] ?? '',
    imageUrl:  j['im'] as String?,
  );

  String? get noImageMessage {
    if (imageUrl != null) return null;
    return '🗿 No image available for this sculpture';
  }
}

Future<List<SculptureData>> loadSculptures() async {
  final raw = await rootBundle.loadString('assets/art/sculptures.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SculptureData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SculptureData>? _shuffledCache;

SculptureData dailySculpture(List<SculptureData> sculptures) {
  if (_shuffledCache == null) {
    final list = List<SculptureData>.from(sculptures);
    final rng = math.Random(20260201);
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
