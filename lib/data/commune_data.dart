import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class CommuneData {
  final String name, department, region, famousFor;
  final int? population, area;
  final String? imageUrl;

  const CommuneData({
    required this.name, required this.department,
    required this.region, required this.famousFor,
    this.population, this.area, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '🏘️ No image available for this commune';

  factory CommuneData.fromJson(Map<String, dynamic> j) => CommuneData(
    name:       j['n']  ?? '',
    department: j['de'] ?? '',
    region:     j['rg'] ?? '',
    population: (j['po'] as num?)?.toInt(),
    area:       (j['ar'] as num?)?.toInt(),
    famousFor:  j['fa'] ?? '',
    imageUrl:   j['im'] as String?,
  );
}

Future<List<CommuneData>> loadCommunes() async {
  final raw = await rootBundle.loadString('assets/world/communes.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => CommuneData.fromJson(e as Map<String, dynamic>)).toList();
}

List<CommuneData>? _shuffledCache;

CommuneData dailyCommune(List<CommuneData> communes) {
  if (_shuffledCache == null) {
    final list = List<CommuneData>.from(communes);
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
