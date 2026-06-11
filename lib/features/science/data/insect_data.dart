import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class InsectData {
  final String name, order, family, habitat, diet, size, famousFor;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '🦟 No image available for this insect';

  const InsectData({
    required this.name, required this.order, required this.family,
    required this.habitat, required this.diet, required this.size,
    required this.famousFor, this.imageUrl,
  });

  factory InsectData.fromJson(Map<String, dynamic> j) => InsectData(
    name:      j['n']   ?? '',
    order:     j['ord'] ?? '',
    family:    j['fam'] ?? '',
    habitat:   j['ha']  ?? '',
    diet:      j['di']  ?? '',
    size:      j['si']  ?? '',
    famousFor: j['ff']  ?? '',
    imageUrl:  j['im']  as String?,
  );
}

Future<List<InsectData>> loadInsects() async {
  final raw = await rootBundle.loadString('assets/science/insects.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => InsectData.fromJson(e as Map<String, dynamic>)).toList();
}

List<InsectData>? _shuffledCache;

InsectData dailyInsect(List<InsectData> insects) {
  if (_shuffledCache == null) {
    final list = List<InsectData>.from(insects);
    final rng = math.Random(20260611);
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
