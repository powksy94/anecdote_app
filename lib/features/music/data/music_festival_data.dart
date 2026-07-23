import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MusicFestivalData {
  final String name, location, attendance, fact;
  final String? imageUrl;

  const MusicFestivalData({
    required this.name, required this.location, required this.attendance,
    required this.fact, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '🎪 No image available for this festival';

  factory MusicFestivalData.fromJson(Map<String, dynamic> j) => MusicFestivalData(
    name:       j['n']   ?? '',
    location:   j['loc'] ?? '',
    attendance: j['at']  ?? '',
    fact:       j['fa']  ?? '',
    imageUrl:   j['im'] as String?,
  );
}

Future<List<MusicFestivalData>> loadMusicFestivals() async {
  final raw = await rootBundle.loadString('assets/music/music_festivals.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MusicFestivalData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MusicFestivalData>? _shuffledCache;

MusicFestivalData dailyMusicFestival(List<MusicFestivalData> festivals) {
  if (_shuffledCache == null) {
    final list = List<MusicFestivalData>.from(festivals);
    final rng = math.Random(20260204);
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
