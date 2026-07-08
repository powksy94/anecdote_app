import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class ClassicGameData {
  final String name, developer, genre, famousFor;
  final int year;
  final String? imageUrl;
  final String? noImageMessage;

  const ClassicGameData({
    required this.name, required this.year, required this.developer,
    required this.genre, required this.famousFor,
    this.imageUrl, this.noImageMessage,
  });

  factory ClassicGameData.fromJson(Map<String, dynamic> j) => ClassicGameData(
    name:           j['n']   ?? '',
    year:           (j['y'] as num).toInt(),
    developer:      j['de']  ?? '',
    genre:          j['ge']  ?? '',
    famousFor:      j['fa']  ?? '',
    imageUrl:       j['im']  as String?,
    noImageMessage: j['nim'] as String?,
  );
}

Future<List<ClassicGameData>> loadClassicGames() async {
  final raw = await rootBundle.loadString('assets/gaming/classic_games.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => ClassicGameData.fromJson(e as Map<String, dynamic>)).toList();
}

List<ClassicGameData>? _shuffledCache;

ClassicGameData dailyClassicGame(List<ClassicGameData> items) {
  if (_shuffledCache == null) {
    final list = List<ClassicGameData>.from(items);
    final rng = math.Random(20260203);
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
