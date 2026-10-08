import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, rs=reign start (year, negative for BCE), re=reign end (year, negative for BCE),
// fa=famous for, hn=historical note (optional), im=imageUrl

class ChineseDynastyData {
  final String name, famousFor;
  final String? imageUrl, historicalNote;
  final int reignStart, reignEnd;

  const ChineseDynastyData({
    required this.name, required this.famousFor,
    required this.reignStart, required this.reignEnd, this.imageUrl,
    this.historicalNote,
  });

  String? get noImageMessage => imageUrl != null ? null : '🏮 No image available for this dynasty';

  /// Formats a year as "123 BCE", or just "123" for a common-era year (the "CE" suffix
  /// is conventionally omitted, only BCE needs to be made explicit).
  static String formatYear(int year) => year < 0 ? '${-year} BCE' : '$year';

  factory ChineseDynastyData.fromJson(Map<String, dynamic> j) => ChineseDynastyData(
    name:        j['n']  ?? '',
    reignStart:  (j['rs'] as num?)?.toInt() ?? 0,
    reignEnd:    (j['re'] as num?)?.toInt() ?? 0,
    famousFor:   j['fa'] ?? '',
    imageUrl:    j['im'] as String?,
    historicalNote: j['hn'] as String?,
  );
}

Future<List<ChineseDynastyData>> loadChineseDynasties() async {
  final raw = await rootBundle.loadString('assets/history/chinese_dynasties.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => ChineseDynastyData.fromJson(e as Map<String, dynamic>)).toList();
}

List<ChineseDynastyData>? _shuffledCache;

ChineseDynastyData dailyChineseDynasty(List<ChineseDynastyData> dynasties) {
  if (_shuffledCache == null) {
    final list = List<ChineseDynastyData>.from(dynasties);
    final rng = math.Random(20261003);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 10, 3);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
