import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MedicationData {
  final String name, family, discoveryYear, mechanism, administration, indications, sideEffects, fact;

  const MedicationData({
    required this.name, required this.family, required this.discoveryYear,
    required this.mechanism, required this.administration, required this.indications,
    required this.sideEffects, required this.fact,
  });

  factory MedicationData.fromJson(Map<String, dynamic> j) => MedicationData(
    name:            j['n']   ?? '',
    family:          j['fam'] ?? '',
    discoveryYear:   j['yr']  ?? '',
    mechanism:       j['moa'] ?? '',
    administration:  j['adm'] ?? '',
    indications:     j['ind'] ?? '',
    sideEffects:     j['se']  ?? '',
    fact:            j['fa']  ?? '',
  );
}

Future<List<MedicationData>> loadMedications() async {
  final raw = await rootBundle.loadString('assets/health/medications.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MedicationData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MedicationData>? _shuffledCache;

MedicationData dailyMedication(List<MedicationData> medications) {
  if (_shuffledCache == null) {
    final list = List<MedicationData>.from(medications);
    final rng = math.Random(20260405);
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
