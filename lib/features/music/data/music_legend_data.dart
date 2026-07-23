import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MusicLegendData {
  final String name, genre, famousFor;
  final String? imageUrl, warningLevel, warningText;

  const MusicLegendData({
    required this.name, required this.genre, required this.famousFor,
    this.imageUrl, this.warningLevel, this.warningText,
  });

  String? get noImageMessage => imageUrl != null ? null : '🎤 No portrait available for this artist';

  factory MusicLegendData.fromJson(Map<String, dynamic> j) => MusicLegendData(
    name:         j['n']  ?? '',
    genre:        j['gn'] ?? '',
    famousFor:    j['fa'] ?? '',
    imageUrl:     j['im'] as String?,
    warningLevel: j['wl'] as String?,
    warningText:  j['wi'] as String?,
  );
}

Future<List<MusicLegendData>> loadMusicLegends() async {
  final raw = await rootBundle.loadString('assets/music/music_legends.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MusicLegendData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MusicLegendData>? _shuffledCache;

MusicLegendData dailyMusicLegend(List<MusicLegendData> legends) {
  if (_shuffledCache == null) {
    final list = List<MusicLegendData>.from(legends);
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
