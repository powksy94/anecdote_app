import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class AmericanPresidentData {
  final String name, party, state, vicePresident, famousFor;
  final String? imageUrl;
  final int number, termStart;
  final int? termEnd, mandateNumber;

  const AmericanPresidentData({
    required this.name, required this.number, required this.party,
    required this.state, required this.vicePresident, required this.famousFor,
    required this.termStart, this.termEnd, this.mandateNumber, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '🇺🇸 No portrait available for this president';

  factory AmericanPresidentData.fromJson(Map<String, dynamic> j) =>
      AmericanPresidentData(
    name:          j['n']  ?? '',
    number:        (j['nu'] as num?)?.toInt() ?? 0,
    termStart:     (j['ts'] as num?)?.toInt() ?? 0,
    termEnd:       (j['te'] as num?)?.toInt(),
    party:         j['pa'] ?? '',
    state:         j['st'] ?? '',
    vicePresident: j['vp'] ?? '',
    famousFor:     j['fa'] ?? '',
    mandateNumber: (j['mn'] as num?)?.toInt(),
    imageUrl:      j['im'] as String?,
  );
}

Future<List<AmericanPresidentData>> loadAmericanPresidents() async {
  final raw = await rootBundle.loadString('assets/history/american_presidents.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => AmericanPresidentData.fromJson(e as Map<String, dynamic>)).toList();
}

List<AmericanPresidentData>? _shuffledCache;

AmericanPresidentData dailyPresident(List<AmericanPresidentData> presidents) {
  if (_shuffledCache == null) {
    final list = List<AmericanPresidentData>.from(presidents);
    final rng = math.Random(20260107);
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
