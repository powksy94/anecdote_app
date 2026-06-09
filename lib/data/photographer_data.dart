import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, na=nationality, bo=born, di=died, st=style, fw=famous_work, fa=famous_for, im=imageUrl, wl=warningLevel, wi=warningText

class PhotographerData {
  final String name, nationality, born, died, style, famousWork, famousFor;
  final String? imageUrl;
  final String? warningLevel;
  final String? warningText;

  const PhotographerData({
    required this.name, required this.nationality, required this.born,
    required this.died, required this.style, required this.famousWork,
    required this.famousFor, this.imageUrl, this.warningLevel, this.warningText,
  });

  factory PhotographerData.fromJson(Map<String, dynamic> j) => PhotographerData(
    name:         j['n']  ?? '',
    nationality:  j['na'] ?? '',
    born:         j['bo'] ?? '',
    died:         j['di'] ?? '',
    style:        j['st'] ?? '',
    famousWork:   j['fw'] ?? '',
    famousFor:    j['fa'] ?? '',
    imageUrl:     j['im'] as String?,
    warningLevel: j['wl'] as String?,
    warningText:  j['wi'] as String?,
  );

  String? get noImageMessage {
    if (imageUrl != null) return null;
    return '📷 No image available for this photographer';
  }
}

Future<List<PhotographerData>> loadPhotographers() async {
  final raw = await rootBundle.loadString('assets/art/photographers.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => PhotographerData.fromJson(e as Map<String, dynamic>)).toList();
}

List<PhotographerData>? _shuffledCache;

PhotographerData dailyPhotographer(List<PhotographerData> photographers) {
  if (_shuffledCache == null) {
    final list = List<PhotographerData>.from(photographers);
    final rng = math.Random(20260204);
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
