import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class ChemicalElementData {
  final String name, symbol, atomicMass, category, discovered, discoveredBy, state, famousFor;
  final int atomicNumber, group, period;
  final String? imageUrl;

  String? get noImageMessage => imageUrl != null ? null : '⚗️ No sample image available for this element';

  const ChemicalElementData({
    required this.name, required this.symbol, required this.atomicNumber,
    required this.atomicMass, required this.category, required this.group,
    required this.period, required this.discovered, required this.discoveredBy,
    required this.state, required this.famousFor, this.imageUrl,
  });

  factory ChemicalElementData.fromJson(Map<String, dynamic> j) => ChemicalElementData(
    name:          j['n']  ?? '',
    symbol:        j['sy'] ?? '',
    atomicNumber:  (j['an'] as num?)?.toInt() ?? 0,
    atomicMass:    j['am']?.toString() ?? '',
    category:      j['ca'] ?? '',
    group:         (j['gr'] as num?)?.toInt() ?? 0,
    period:        (j['pe'] as num?)?.toInt() ?? 0,
    discovered:    j['di']?.toString() ?? '',
    discoveredBy:  j['db'] ?? '',
    state:         j['st'] ?? '',
    famousFor:     j['fa'] ?? '',
    imageUrl:      j['im'] as String?,
  );
}

Future<List<ChemicalElementData>> loadChemicalElements() async {
  final raw = await rootBundle.loadString('assets/science/chemical_elements.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => ChemicalElementData.fromJson(e as Map<String, dynamic>)).toList();
}

List<ChemicalElementData>? _shuffledCache;

ChemicalElementData dailyChemicalElement(List<ChemicalElementData> elements) {
  if (_shuffledCache == null) {
    final list = List<ChemicalElementData>.from(elements);
    final rng = math.Random(20260201);
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
