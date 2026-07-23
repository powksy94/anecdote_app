import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MusicAwardData {
  final String title, artist, award, fact;
  final String? imageUrl;
  final int year;

  const MusicAwardData({
    required this.title, required this.artist, required this.award,
    required this.fact, required this.year, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '🏆 No image available for this award';

  factory MusicAwardData.fromJson(Map<String, dynamic> j) => MusicAwardData(
    title:    j['n']  ?? '',
    artist:   j['ar'] ?? '',
    award:    j['aw'] ?? '',
    fact:     j['fa'] ?? '',
    year:     (j['yr'] as num?)?.toInt() ?? 0,
    imageUrl: j['im'] as String?,
  );
}

Future<List<MusicAwardData>> loadMusicAwards() async {
  final raw = await rootBundle.loadString('assets/music/music_awards.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MusicAwardData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MusicAwardData>? _shuffledCache;

MusicAwardData dailyMusicAward(List<MusicAwardData> awards) {
  if (_shuffledCache == null) {
    final list = List<MusicAwardData>.from(awards);
    final rng = math.Random(20260205);
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
