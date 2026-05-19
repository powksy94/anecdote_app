import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';
import '../models/content_type.dart';

class CinemaQuoteData {
  final String quote, quoteLang, film, character, actor, director, timing, context;
  final int year;
  final String? type, qEn, qFr, qEs;

  const CinemaQuoteData({
    required this.quote, required this.quoteLang, required this.film,
    required this.character, required this.actor, required this.director,
    required this.year, required this.timing, required this.context,
    this.type, this.qEn, this.qFr, this.qEs,
  });

  factory CinemaQuoteData.fromJson(Map<String, dynamic> j) => CinemaQuoteData(
    quote:      j['q']  ?? '',
    quoteLang:  j['ql'] ?? 'en',
    film:       j['fi'] ?? '',
    character:  j['ch'] ?? '',
    actor:      j['ac'] ?? '',
    director:   j['di'] ?? '',
    year:       (j['yr'] as num?)?.toInt() ?? 0,
    type:       j['ty'] as String?,
    timing:     j['ti'] ?? '',
    context:    j['co'] ?? '',
    qEn:        j['q_en'] as String?,
    qFr:        j['q_fr'] as String?,
    qEs:        j['q_es'] as String?,
  );

  /// Retourne la traduction dans la locale donnée, ou null si VO = locale.
  String? translationFor(String locale) {
    if (quoteLang == locale) return null;
    switch (locale) {
      case 'fr': return qFr;
      case 'es': return qEs;
      default:   return qEn;
    }
  }
}

Future<List<CinemaQuoteData>> _loadFile(String asset) async {
  final raw = await rootBundle.loadString(asset);
  final list = jsonDecode(raw) as List;
  return list.map((e) => CinemaQuoteData.fromJson(e as Map<String, dynamic>)).toList();
}

List<CinemaQuoteData>? _classicCache;
List<CinemaQuoteData>? _cache80s90s;
List<CinemaQuoteData>? _modernCache;

Future<List<CinemaQuoteData>> loadCinemaQuotes(ContentType type) async {
  switch (type) {
    case ContentType.classicCinema:
      _classicCache ??= await _loadFile('assets/quotes_classic.json');
      return _classicCache!;
    case ContentType.cinema80s90s:
      _cache80s90s ??= await _loadFile('assets/quotes_80s90s.json');
      return _cache80s90s!;
    case ContentType.modernCinema:
      _modernCache ??= await _loadFile('assets/quotes_modern.json');
      return _modernCache!;
    default:
      return [];
  }
}

final Map<ContentType, List<CinemaQuoteData>?> _shuffledCaches = {};

CinemaQuoteData dailyCinemaQuote(List<CinemaQuoteData> quotes, ContentType type) {
  if (_shuffledCaches[type] == null) {
    final seeds = {
      ContentType.classicCinema: 20260108,
      ContentType.cinema80s90s:  20260109,
      ContentType.modernCinema:  20260110,
    };
    final list = List<CinemaQuoteData>.from(quotes);
    final rng = math.Random(seeds[type] ?? 20260108);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCaches[type] = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 1, 1);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCaches[type]![index % _shuffledCaches[type]!.length];
}
