import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class GamingNominationData {
  final int year;
  final String category, name, developer, awardBody, description;
  final String? imageUrl;
  final String? noImageMessage;

  const GamingNominationData({
    required this.year, required this.category, required this.name,
    required this.developer, required this.awardBody, required this.description,
    this.imageUrl, this.noImageMessage,
  });

  factory GamingNominationData.fromJson(Map<String, dynamic> j) =>
      GamingNominationData(
        year:           (j['y'] as num).toInt(),
        category:       j['cat'] ?? '',
        name:           j['n']   ?? '',
        developer:      j['de']  ?? '',
        awardBody:      j['aw']  ?? '',
        description:    j['fa']  ?? '',
        imageUrl:       j['im']  as String?,
        noImageMessage: j['nim'] as String?,
      );
}

Future<List<GamingNominationData>> loadGamingNominations() async {
  final raw = await rootBundle.loadString('assets/gaming/gaming_nominations.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => GamingNominationData.fromJson(e as Map<String, dynamic>)).toList();
}

List<GamingNominationData>? _shuffledCache;

GamingNominationData dailyGamingNomination(List<GamingNominationData> items) {
  if (_shuffledCache == null) {
    final list = List<GamingNominationData>.from(items);
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
