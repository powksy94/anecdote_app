import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class IndependentMusicianData {
  final String name, genre, famousSong, famousFor;
  final String? imageUrl;

  const IndependentMusicianData({
    required this.name, required this.genre, required this.famousSong,
    required this.famousFor, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '🎤 No portrait available for this artist';

  factory IndependentMusicianData.fromJson(Map<String, dynamic> j) => IndependentMusicianData(
    name:       j['n']  ?? '',
    genre:      j['gn'] ?? '',
    famousSong: j['fs'] ?? '',
    famousFor:  j['fa'] ?? '',
    imageUrl:   j['im'] as String?,
  );
}

Future<List<IndependentMusicianData>> loadIndependentMusicians() async {
  final raw = await rootBundle.loadString('assets/music/independent_musicians.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => IndependentMusicianData.fromJson(e as Map<String, dynamic>)).toList();
}

List<IndependentMusicianData>? _shuffledCache;

IndependentMusicianData dailyIndependentMusician(List<IndependentMusicianData> artists) {
  if (_shuffledCache == null) {
    final list = List<IndependentMusicianData>.from(artists);
    final rng = math.Random(20260703);
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
