import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MythologicalCreatureData {
  final String name, origin, fact, defeatedBy;
  final String? imageUrl;

  const MythologicalCreatureData({
    required this.name, required this.origin, required this.fact,
    required this.defeatedBy, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '🐉 No image available for this creature';

  factory MythologicalCreatureData.fromJson(Map<String, dynamic> j) => MythologicalCreatureData(
    name:        j['n']      ?? '',
    origin:      j['origin'] ?? '',
    fact:        j['fa']     ?? '',
    defeatedBy:  j['df']     ?? '',
    imageUrl:    j['im'] as String?,
  );
}

Future<List<MythologicalCreatureData>> loadMythologicalCreatures() async {
  final raw = await rootBundle.loadString('assets/mythology/mythological_creatures.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MythologicalCreatureData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MythologicalCreatureData>? _shuffledCache;

MythologicalCreatureData dailyMythologicalCreature(List<MythologicalCreatureData> creatures) {
  if (_shuffledCache == null) {
    final list = List<MythologicalCreatureData>.from(creatures);
    final rng = math.Random(20260304);
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
