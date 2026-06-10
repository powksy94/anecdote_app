import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class PaintingData {
  final String title, artist, year, medium, style, museum, famousFor;
  final String? imageUrl;

  const PaintingData({
    required this.title, required this.artist, required this.year,
    required this.medium, required this.style, required this.museum,
    required this.famousFor, this.imageUrl,
  });

  factory PaintingData.fromJson(Map<String, dynamic> j) => PaintingData(
    title:     j['n']  ?? '',
    artist:    j['ar'] ?? '',
    year:      j['yr'] ?? '',
    medium:    j['me'] ?? '',
    style:     j['st'] ?? '',
    museum:    j['mu'] ?? '',
    famousFor: j['fa'] ?? '',
    imageUrl:  j['im'] as String?,
  );

  String? get noImageMessage {
    if (imageUrl != null) return null;
    return '🖼️ No digital reproduction available for this artwork';
  }
}

Future<List<PaintingData>> loadPaintings() async {
  final raw = await rootBundle.loadString('assets/art/paintings.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => PaintingData.fromJson(e as Map<String, dynamic>)).toList();
}

List<PaintingData>? _shuffledCache;

PaintingData dailyPainting(List<PaintingData> paintings) {
  if (_shuffledCache == null) {
    final list = List<PaintingData>.from(paintings);
    final rng = math.Random(20260114);
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
