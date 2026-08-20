import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class HorrorCinemaData {
  final String title, director, country, famousFor;
  final int year, duration;
  final String? imageUrl, titleFr, titleEs;

  String? get noImageMessage => imageUrl != null ? null : '🎬 No poster available for this film';

  const HorrorCinemaData({
    required this.title, required this.director, required this.country,
    required this.year, required this.duration, required this.famousFor,
    this.imageUrl, this.titleFr, this.titleEs,
  });

  factory HorrorCinemaData.fromJson(Map<String, dynamic> j) => HorrorCinemaData(
    title:     j['n']  ?? '',
    director:  j['di'] ?? '',
    country:   j['co'] ?? '',
    year:      (j['y'] as num?)?.toInt() ?? 0,
    duration:  (j['du'] as num?)?.toInt() ?? 0,
    famousFor: j['fa'] ?? '',
    imageUrl:  j['im'] as String?,
    titleFr:   j['n_fr'] as String?,
    titleEs:   j['n_es'] as String?,
  );
}

Future<List<HorrorCinemaData>> loadHorrorCinema() async {
  final raw = await rootBundle.loadString('assets/cinema/horror_films.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => HorrorCinemaData.fromJson(e as Map<String, dynamic>)).toList();
}

List<HorrorCinemaData>? _shuffledCache;

HorrorCinemaData dailyHorrorCinema(List<HorrorCinemaData> films) {
  if (_shuffledCache == null) {
    final list = List<HorrorCinemaData>.from(films);
    final rng = math.Random(20260701);
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
