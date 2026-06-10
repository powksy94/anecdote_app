import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class StateData {
  final String name, capital, nickname, region, famousFor;
  final int population, area, statehoodYear;
  final String? imageUrl;

  const StateData({
    required this.name, required this.capital, required this.nickname,
    required this.region, required this.famousFor,
    required this.population, required this.area, required this.statehoodYear,
    this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '🗺️ No image available for this state';

  factory StateData.fromJson(Map<String, dynamic> j) => StateData(
    name:          j['n']  ?? '',
    capital:       j['ca'] ?? '',
    nickname:      j['ni'] ?? '',
    region:        j['re'] ?? '',
    population:    (j['po'] as num?)?.toInt() ?? 0,
    area:          (j['ar'] as num?)?.toInt() ?? 0,
    statehoodYear: (j['sy'] as num?)?.toInt() ?? 0,
    famousFor:     j['fa'] ?? '',
    imageUrl:      j['im'] as String?,
  );
}

Future<List<StateData>> loadStates() async {
  final raw = await rootBundle.loadString('assets/world/american_states.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => StateData.fromJson(e as Map<String, dynamic>)).toList();
}

List<StateData>? _shuffledCache;

StateData dailyState(List<StateData> states) {
  if (_shuffledCache == null) {
    final list = List<StateData>.from(states);
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
