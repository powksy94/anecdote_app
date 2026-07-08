import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class BannedGameData {
  final String name, developer, bannedIn, reason;
  final int year;
  final String? imageUrl;
  final String? noImageMessage;

  const BannedGameData({
    required this.name, required this.year, required this.developer,
    required this.bannedIn, required this.reason,
    this.imageUrl, this.noImageMessage,
  });

  factory BannedGameData.fromJson(Map<String, dynamic> j) => BannedGameData(
    name:           j['n']   ?? '',
    year:           (j['y'] as num).toInt(),
    developer:      j['de']  ?? '',
    bannedIn:       j['ban'] ?? '',
    reason:         j['rea'] ?? '',
    imageUrl:       j['im']  as String?,
    noImageMessage: j['nim'] as String?,
  );
}

Future<List<BannedGameData>> loadBannedGames() async {
  final raw = await rootBundle.loadString('assets/gaming/banned_games.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => BannedGameData.fromJson(e as Map<String, dynamic>)).toList();
}

List<BannedGameData>? _shuffledCache;

BannedGameData dailyBannedGame(List<BannedGameData> items) {
  if (_shuffledCache == null) {
    final list = List<BannedGameData>.from(items);
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
