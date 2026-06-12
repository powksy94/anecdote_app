import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class CloudData {
  final String name, category, altitude, volume, conditions,
      appearance, weather, famousFor;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '☁️ No image available for this cloud type';

  const CloudData({
    required this.name, required this.category, required this.altitude,
    required this.volume, required this.conditions, required this.appearance,
    required this.weather, required this.famousFor,
    this.imageUrl,
  });

  factory CloudData.fromJson(Map<String, dynamic> j) => CloudData(
    name:       j['n']    ?? '',
    category:   j['cat']  ?? '',
    altitude:   j['alt']  ?? '',
    volume:     j['vol']  ?? '',
    conditions: j['cond'] ?? '',
    appearance: j['ap']   ?? '',
    weather:    j['aw']   ?? '',
    famousFor:  j['ff']   ?? '',
    imageUrl:   j['im']   as String?,
  );
}

Future<List<CloudData>> loadClouds() async {
  final raw = await rootBundle.loadString('assets/science/clouds.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => CloudData.fromJson(e as Map<String, dynamic>)).toList();
}

List<CloudData>? _shuffledCache;

CloudData dailyCloud(List<CloudData> clouds) {
  if (_shuffledCache == null) {
    final list = List<CloudData>.from(clouds);
    final rng = math.Random(20260615);
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
