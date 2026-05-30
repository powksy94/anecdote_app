import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class SpaceMissionData {
  final String name, agency, destination, duration, status, famousFor;
  final int launchYear;
  final String? imageUrl;

  const SpaceMissionData({
    required this.name, required this.agency, required this.destination,
    required this.duration, required this.status, required this.famousFor,
    required this.launchYear, this.imageUrl,
  });

  factory SpaceMissionData.fromJson(Map<String, dynamic> j) => SpaceMissionData(
    name:        j['n']  ?? '',
    agency:      j['ag'] ?? '',
    destination: j['ds'] ?? '',
    launchYear:  (j['la'] as num?)?.toInt() ?? 0,
    duration:    j['du'] ?? '',
    status:      j['st'] ?? '',
    famousFor:   j['fa'] ?? '',
    imageUrl:    j['im'] as String?,
  );
}

Future<List<SpaceMissionData>> loadSpaceMissions() async {
  final raw = await rootBundle.loadString('assets/space/missions.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => SpaceMissionData.fromJson(e as Map<String, dynamic>)).toList();
}

List<SpaceMissionData>? _shuffledCache;

SpaceMissionData dailySpaceMission(List<SpaceMissionData> missions) {
  if (_shuffledCache == null) {
    final list = List<SpaceMissionData>.from(missions);
    final rng = math.Random(20260112);
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
