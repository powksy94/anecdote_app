import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=invention name, inv=inventor(s) credited (null if anonymous), cc=ISO2 country code(s)
// ("/"-joined when several, null if no meaningful country), yr=year or approximate date,
// fa=fact, im=imageUrl (picture of the invention, not a portrait of its inventor)

class AccidentalInventionData {
  final String name, year, fact;
  final String? inventor;
  final String? countryCode;
  final String? imageUrl;

  const AccidentalInventionData({
    required this.name, required this.year, required this.fact,
    this.inventor, this.countryCode, this.imageUrl,
  });

  factory AccidentalInventionData.fromJson(Map<String, dynamic> j) => AccidentalInventionData(
    name:        j['n']   as String,
    year:        j['yr']  as String,
    fact:        j['fa']  as String,
    inventor:    j['inv'] as String?,
    countryCode: j['cc']  as String?,
    imageUrl:    (j['im'] as String?)?.isEmpty == true ? null : j['im'] as String?,
  );
}

Future<List<AccidentalInventionData>> loadAccidentalInventions() async {
  final raw = await rootBundle.loadString('assets/tech/accidental_inventions.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => AccidentalInventionData.fromJson(e as Map<String, dynamic>)).toList();
}

List<AccidentalInventionData>? _shuffledCache;

AccidentalInventionData dailyAccidentalInvention(List<AccidentalInventionData> items) {
  if (_shuffledCache == null) {
    final list = List<AccidentalInventionData>.from(items);
    final rng = math.Random(20261113);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 11, 13);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
