import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class BirdData {
  final String name, order, family, habitat, diet, size, speed, famousFor;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '🐦 No image available for this bird';

  const BirdData({
    required this.name, required this.order, required this.family,
    required this.habitat, required this.diet, required this.size,
    required this.speed, required this.famousFor, this.imageUrl,
  });

  factory BirdData.fromJson(Map<String, dynamic> j) => BirdData(
    name:      j['n']   ?? '',
    order:     j['ord'] ?? '',
    family:    j['fam'] ?? '',
    habitat:   j['ha']  ?? '',
    diet:      j['di']  ?? '',
    size:      j['si']  ?? '',
    speed:     j['sp']  ?? '',
    famousFor: j['ff']  ?? '',
    imageUrl:  j['im']  as String?,
  );
}

Future<List<BirdData>> loadBirds() async {
  final raw = await rootBundle.loadString('assets/science/birds.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => BirdData.fromJson(e as Map<String, dynamic>)).toList();
}

List<BirdData>? _shuffledCache;

BirdData dailyBird(List<BirdData> birds) {
  if (_shuffledCache == null) {
    final list = List<BirdData>.from(birds);
    final rng = math.Random(20260612);
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
