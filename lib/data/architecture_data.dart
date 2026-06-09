import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, ac=architect, yr=year, lo=location, st=style, co=country, fa=famous_for, im=imageUrl

class ArchitectureData {
  final String name, architect, year, location, style, country, famousFor;
  final String? imageUrl;

  const ArchitectureData({
    required this.name, required this.architect, required this.year,
    required this.location, required this.style, required this.country,
    required this.famousFor, this.imageUrl,
  });

  factory ArchitectureData.fromJson(Map<String, dynamic> j) => ArchitectureData(
    name:      j['n']  ?? '',
    architect: j['ac'] ?? '',
    year:      j['yr'] ?? '',
    location:  j['lo'] ?? '',
    style:     j['st'] ?? '',
    country:   j['co'] ?? '',
    famousFor: j['fa'] ?? '',
    imageUrl:  j['im'] as String?,
  );

  String? get noImageMessage {
    if (imageUrl != null) return null;
    return '🏛️ No image available for this building';
  }
}

Future<List<ArchitectureData>> loadArchitecture() async {
  final raw = await rootBundle.loadString('assets/art/architecture.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => ArchitectureData.fromJson(e as Map<String, dynamic>)).toList();
}

List<ArchitectureData>? _shuffledCache;

ArchitectureData dailyArchitecture(List<ArchitectureData> items) {
  if (_shuffledCache == null) {
    final list = List<ArchitectureData>.from(items);
    final rng = math.Random(20260202);
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
