import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MentalMedicationData {
  final String name, family, discoveryYear, mechanism, administration, indications, sideEffects, fact;

  const MentalMedicationData({
    required this.name, required this.family, required this.discoveryYear,
    required this.mechanism, required this.administration, required this.indications,
    required this.sideEffects, required this.fact,
  });

  factory MentalMedicationData.fromJson(Map<String, dynamic> j) => MentalMedicationData(
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

Future<List<MentalMedicationData>> loadMentalMedications() async {
  final raw = await rootBundle.loadString('assets/health/mental_medications.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MentalMedicationData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MentalMedicationData>? _shuffledCache;

MentalMedicationData dailyMentalMedication(List<MentalMedicationData> medications) {
  if (_shuffledCache == null) {
    final list = List<MentalMedicationData>.from(medications);
    final rng = math.Random(20260406);
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
