import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class HumanBoneData {
  final String name, region, count, type, function, famousFor;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '🦴 No image available for this bone';

  const HumanBoneData({
    required this.name, required this.region, required this.count,
    required this.type, required this.function, required this.famousFor,
    this.imageUrl,
  });

  factory HumanBoneData.fromJson(Map<String, dynamic> j) => HumanBoneData(
    name:      j['n']   ?? '',
    region:    j['reg'] ?? '',
    count:     j['cnt'] ?? '',
    type:      j['tp']  ?? '',
    function:  j['fn']  ?? '',
    famousFor: j['ff']  ?? '',
    imageUrl:  j['im']  as String?,
  );
}

Future<List<HumanBoneData>> loadHumanBones() async {
  final raw = await rootBundle.loadString('assets/science/human_bones.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => HumanBoneData.fromJson(e as Map<String, dynamic>)).toList();
}

List<HumanBoneData>? _shuffledCache;

HumanBoneData dailyHumanBone(List<HumanBoneData> bones) {
  if (_shuffledCache == null) {
    final list = List<HumanBoneData>.from(bones);
    final rng = math.Random(20260616);
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
