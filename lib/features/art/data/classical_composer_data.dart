import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, na=nationality, bo=born, di=died, pe=period, fw=famous_works, fa=famous_for, im=imageUrl

class ClassicalComposerData {
  final String name, nationality, born, died, period, famousWorks, famousFor;
  final String? imageUrl;

  const ClassicalComposerData({
    required this.name, required this.nationality, required this.born,
    required this.died, required this.period, required this.famousWorks,
    required this.famousFor, this.imageUrl,
  });

  factory ClassicalComposerData.fromJson(Map<String, dynamic> j) => ClassicalComposerData(
    name:        j['n']  ?? '',
    nationality: j['na'] ?? '',
    born:        j['bo'] ?? '',
    died:        j['di'] ?? '',
    period:      j['pe'] ?? '',
    famousWorks: j['fw'] ?? '',
    famousFor:   j['fa'] ?? '',
    imageUrl:    j['im'] as String?,
  );

  String? get noImageMessage {
    if (imageUrl != null) return null;
    return '🎵 No image available for this composer';
  }
}

Future<List<ClassicalComposerData>> loadClassicalComposers() async {
  final raw = await rootBundle.loadString('assets/art/classical_composers.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => ClassicalComposerData.fromJson(e as Map<String, dynamic>)).toList();
}

List<ClassicalComposerData>? _shuffledCache;

ClassicalComposerData dailyClassicalComposer(List<ClassicalComposerData> composers) {
  if (_shuffledCache == null) {
    final list = List<ClassicalComposerData>.from(composers);
    final rng = math.Random(20260205);
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
