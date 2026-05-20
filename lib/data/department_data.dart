import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class DepartmentData {
  final String code, name, prefecture, region;
  final int? population, area;

  const DepartmentData({
    required this.code, required this.name,
    required this.prefecture, required this.region,
    this.population, this.area,
  });

  factory DepartmentData.fromJson(Map<String, dynamic> j) => DepartmentData(
    code:       j['co'] ?? '', 
    name:       j['n']  ?? '', 
    prefecture: j['pr'] ?? '', 
    region:     j['re'] ?? '',
    population: (j['po'] as num?)?.toInt(),
    area:       (j['ar'] as num?)?.toInt(),
  );
}

Future<List<DepartmentData>> loadDepartments() async {
  final raw = await rootBundle.loadString('assets/world/french_departments.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => DepartmentData.fromJson(e as Map<String, dynamic>)).toList();
}

List<DepartmentData>? _shuffledCache;

DepartmentData  dailyDepartment(List<DepartmentData> departments) {
  if (_shuffledCache == null) {
    final list = List<DepartmentData>.from(departments);
    final rng = math.Random(20260102);
    for (int i = list.length -1; i > 0; i--) {
      final j = rng.nextInt( i + 1);
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