import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class CountryCurrency {
  final String code, name, symbol;
  const CountryCurrency({required this.code, required this.name, required this.symbol});
  factory CountryCurrency.fromJson(Map<String, dynamic> j) => CountryCurrency(
        code: j['code'] ?? '', name: j['name'] ?? '', symbol: j['symbol'] ?? '');
}

class CountryData {
  final String name, iso2, capital, region;
  final double? area, lifeExpectancy, unemployment, gdp;
  final int? population;
  final CountryCurrency? currency;
  final List<String> languages;

  const CountryData({
    required this.name,
    required this.iso2,
    required this.capital,
    required this.region,
    this.area,
    this.lifeExpectancy,
    this.unemployment,
    this.gdp,
    this.population,
    this.currency,
    required this.languages,
  });

  factory CountryData.fromJson(Map<String, dynamic> j) => CountryData(
        name:           j['n']  ?? '',
        iso2:           j['i2'] ?? '',
        capital:        j['ca'] ?? '',
        region:         j['re'] ?? '',
        area:           (j['ar'] as num?)?.toDouble(),
        population:     (j['po'] as num?)?.toInt(),
        gdp:            (j['gd'] as num?)?.toDouble(),
        lifeExpectancy: (j['le'] as num?)?.toDouble(),
        unemployment:   (j['un'] as num?)?.toDouble(),
        currency:       j['cu'] != null
            ? CountryCurrency.fromJson(j['cu'] as Map<String, dynamic>)
            : null,
        languages: (j['la'] as List?)?.map((e) => e.toString()).toList() ?? [],
      );
}

Future<List<CountryData>> loadCountries() async {
  final raw = await rootBundle.loadString('assets/countries.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => CountryData.fromJson(e as Map<String, dynamic>)).toList();
}

List<CountryData>? _shuffledCache;

CountryData dailyCountry(List<CountryData> countries) {
  if (_shuffledCache == null) {
    final list = List<CountryData>.from(countries);
    final rng = math.Random(20260101);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i];
      list[i] = list[j];
      list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 1, 1);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}
