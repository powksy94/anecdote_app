import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class MedicalAnecdoteData {
  final String title, year, fact;

  const MedicalAnecdoteData({
    required this.title, required this.year, required this.fact,
  });

  factory MedicalAnecdoteData.fromJson(Map<String, dynamic> j) => MedicalAnecdoteData(
    title: j['n']  ?? '',
    year:  j['yr'] ?? '',
    fact:  j['fa'] ?? '',
  );
}

Future<List<MedicalAnecdoteData>> loadMedicalAnecdotes() async {
  final raw = await rootBundle.loadString('assets/health/medical_anecdotes.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => MedicalAnecdoteData.fromJson(e as Map<String, dynamic>)).toList();
}

List<MedicalAnecdoteData>? _shuffledCache;

MedicalAnecdoteData dailyMedicalAnecdote(List<MedicalAnecdoteData> anecdotes) {
  if (_shuffledCache == null) {
    final list = List<MedicalAnecdoteData>.from(anecdotes);
    final rng = math.Random(20260401);
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
