import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class DinosaurData {
  final String name, period, diet, describer, famousFor;
  final double? length;
  final int? weight, discoveryYear;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '🦕 No fossil imagery available for this dinosaur';

  const DinosaurData({
    required this.name, required this.period, required this.diet,
    required this.describer, required this.famousFor,
    this.length, this.weight, this.discoveryYear, this.imageUrl,
  });

  factory DinosaurData.fromJson(Map<String, dynamic> j) => DinosaurData(
    name:          j['n']  ?? '',
    period:        j['pe'] ?? '',
    diet:          j['di'] ?? '',
    length:        (j['le'] as num?)?.toDouble(),
    weight:        (j['we'] as num?)?.toInt(),
    discoveryYear: (j['yr'] as num?)?.toInt(),
    describer:     j['dc'] ?? '',
    famousFor:     j['fa'] ?? '',
    imageUrl:      j['im'] as String?,
  );
}

Future<List<DinosaurData>> loadDinosaurs() async {
  final raw = await rootBundle.loadString('assets/science/dinosaurs.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => DinosaurData.fromJson(e as Map<String, dynamic>)).toList();
}

List<DinosaurData>? _shuffledCache;

DinosaurData dailyDinosaur(List<DinosaurData> dinosaurs) {
  if (_shuffledCache == null) {
    final list = List<DinosaurData>.from(dinosaurs);
    final rng = math.Random(20260111);
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
