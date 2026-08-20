import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class BannedCinemaData {
  final String title, director, bannedIn, reason;
  final int year, duration;
  final List<String> contentTypes;
  final String? imageUrl, titleFr, titleEs;

  String? get noImageMessage => imageUrl != null ? null : '🎬 No poster available for this film';

  const BannedCinemaData({
    required this.title, required this.director, required this.bannedIn,
    required this.year, required this.duration, required this.reason,
    this.contentTypes = const [], this.imageUrl, this.titleFr, this.titleEs,
  });

  factory BannedCinemaData.fromJson(Map<String, dynamic> j) => BannedCinemaData(
    title:        j['n']   ?? '',
    director:     j['di']  ?? '',
    bannedIn:     j['ban'] ?? '',
    year:         (j['y'] as num?)?.toInt() ?? 0,
    duration:     (j['du'] as num?)?.toInt() ?? 0,
    reason:       j['rea'] ?? '',
    contentTypes: (j['ty'] as List?)?.cast<String>() ?? const [],
    imageUrl:     j['im'] as String?,
    titleFr:      j['n_fr'] as String?,
    titleEs:      j['n_es'] as String?,
  );
}

Future<List<BannedCinemaData>> loadBannedCinema() async {
  final raw = await rootBundle.loadString('assets/cinema/banned_films.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => BannedCinemaData.fromJson(e as Map<String, dynamic>)).toList();
}

List<BannedCinemaData>? _shuffledCache;

BannedCinemaData dailyBannedCinema(List<BannedCinemaData> films) {
  if (_shuffledCache == null) {
    final list = List<BannedCinemaData>.from(films);
    final rng = math.Random(20260702);
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
