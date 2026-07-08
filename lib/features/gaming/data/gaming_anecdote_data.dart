import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class GamingAnecdoteData {
  final String name, fact;

  const GamingAnecdoteData({required this.name, required this.fact});

  factory GamingAnecdoteData.fromJson(Map<String, dynamic> j) =>
      GamingAnecdoteData(name: j['n'] ?? '', fact: j['f'] ?? '');
}

Future<List<GamingAnecdoteData>> loadGamingAnecdotes() async {
  final raw = await rootBundle.loadString('assets/gaming/gaming_anecdotes.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => GamingAnecdoteData.fromJson(e as Map<String, dynamic>)).toList();
}

List<GamingAnecdoteData>? _shuffledCache;

GamingAnecdoteData dailyGamingAnecdote(List<GamingAnecdoteData> items) {
  if (_shuffledCache == null) {
    final list = List<GamingAnecdoteData>.from(items);
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
