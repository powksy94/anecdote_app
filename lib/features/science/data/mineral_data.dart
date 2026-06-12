import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MineralData {
  final String name, group, crystalSystem, hardness, color, luster,
      discovery, production, uses, famousFor;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '💎 No image available for this mineral';

  const MineralData({
    required this.name, required this.group, required this.crystalSystem,
    required this.hardness, required this.color, required this.luster,
    required this.discovery, required this.production,
    required this.uses, required this.famousFor, this.imageUrl,
  });

  factory MineralData.fromJson(Map<String, dynamic> j) => MineralData(
    name:         j['n']   ?? '',
    group:        j['grp'] ?? '',
    crystalSystem:j['cs']  ?? '',
    hardness:     j['ha']  ?? '',
    color:        j['co']  ?? '',
    luster:       j['lu']  ?? '',
    discovery:    j['di']  ?? '',
    production:   j['pr']  ?? '',
    uses:         j['us']  ?? '',
    famousFor:    j['ff']  ?? '',
    imageUrl:     j['im']  as String?,
  );
}

Future<List<MineralData>> loadMinerals() async {
  final raw = await rootBundle.loadString('assets/science/minerals.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MineralData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MineralData>? _shuffledCache;

MineralData dailyMineral(List<MineralData> minerals) {
  if (_shuffledCache == null) {
    final list = List<MineralData>.from(minerals);
    final rng = math.Random(20260613);
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
