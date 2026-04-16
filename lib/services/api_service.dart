import 'dart:convert';
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../data/verified_animals.dart';
import '../data/countries.dart';
import 'exoplanet_service.dart';

/// Nombre de jours écoulés depuis le 1er janvier de l'année courante.
/// Utilise UTC pour l'arithmétique afin d'éviter le décalage DST (heure d'été).
int _dayOfYear() {
  final now = DateTime.now();
  final todayUtc = DateTime.utc(now.year, now.month, now.day);
  final startOfYearUtc = DateTime.utc(now.year, 1, 1);
  return todayUtc.difference(startOfYearUtc).inDays;
}

class ApiService {
  final String apiKey;

  ApiService({required this.apiKey});

  String _getEndpoint(ContentType type) {
    switch (type) {
      case ContentType.anecdote:
        return 'https://api.api-ninjas.com/v1/facts';
      case ContentType.chuckNorris:
        return 'https://api.api-ninjas.com/v1/chucknorris';
      case ContentType.advice:
        return 'https://api.api-ninjas.com/v1/quotes';
      case ContentType.history:
        final now = DateTime.now();
        return 'https://api.api-ninjas.com/v1/historicalevents?month=${now.month}&day=${now.day}';
      case ContentType.animals:
        final dayOfYear = _dayOfYear();
        final animalKeys = verifiedAnimals.keys.toList();
        final selectedAnimal = animalKeys[dayOfYear % animalKeys.length];
        return 'https://api.api-ninjas.com/v1/animals?name=${Uri.encodeComponent(selectedAnimal)}';
      case ContentType.country:
        final day = _dayOfYear();
        final selectedCountry = worldCountries[day % worldCountries.length];
        return 'https://api.api-ninjas.com/v1/country?name=${Uri.encodeComponent(selectedCountry)}';
      case ContentType.exoplanet:
        return '';
    }
  }

Future<ContentData> fetchContent(ContentType type) async {
    try {
      if (type == ContentType.exoplanet) {
        return await ExoplanetService().getDailyContent();
      }
      if (type == ContentType.country) {
        return await _fetchCountryContent();
      }
      if (type == ContentType.chuckNorris) {
        return await _fetchChuckNorrisContent();
      }

      final response = await http.get(
        Uri.parse(_getEndpoint(type)),
        headers: {'X-Api-Key': apiKey},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode != 200) {
        throw Exception('Server error (${response.statusCode})');
      }

      final decoded = jsonDecode(response.body);
      return _parseResponse(type, decoded);
    } on http.ClientException {
      throw Exception('Network error');
    } on TimeoutException {
      throw Exception('Request timed out');
    }
  }

  static const String _chuckHistoryKey = 'chuck_norris_history';
  static const int _chuckHistorySize = 30;

  Future<ContentData> _fetchChuckNorrisContent() async {
    final prefs = await SharedPreferences.getInstance();
    final history = prefs.getStringList(_chuckHistoryKey) ?? [];

    String lastJoke = 'No joke';

    for (int attempt = 0; attempt < 5; attempt++) {
      final response = await http.get(
        Uri.parse('https://api.api-ninjas.com/v1/chucknorris'),
        headers: {'X-Api-Key': apiKey},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode != 200) continue;

      final decoded = jsonDecode(response.body);
      if (decoded is! Map) continue;

      final joke = decoded['joke'] as String? ?? '';
      if (joke.isEmpty) continue;

      lastJoke = joke;

      if (!history.contains(joke)) break;
      debugPrint('Chuck Norris duplicate (attempt $attempt), retrying...');
    }

    history.add(lastJoke);
    if (history.length > _chuckHistorySize) history.removeAt(0);
    await prefs.setStringList(_chuckHistoryKey, history);

    return ContentData(preview: lastJoke);
  }

  Future<ContentData> _fetchCountryContent() async {
    final headers = {'X-Api-Key': apiKey};
    final day = _dayOfYear();
    // Le pas de fallback est ~1/5 de la liste pour ne jamais coïncider avec un jour adjacent
    final step = worldCountries.length ~/ 5;

    // Try today's country, then fallbacks at large intervals (never day+1, day+2…)
    for (int offset = 0; offset < 5; offset++) {
      final candidate = worldCountries[(day + offset * step) % worldCountries.length];

      final countryRes = await http.get(
        Uri.parse('https://api.api-ninjas.com/v1/country?name=${Uri.encodeComponent(candidate)}'),
        headers: headers,
      ).timeout(const Duration(seconds: 10));

      if (countryRes.statusCode != 200) {
        debugPrint('Country "$candidate" returned ${countryRes.statusCode}, trying next...');
        continue;
      }

      final decoded = jsonDecode(countryRes.body);
      if (decoded is! List || decoded.isEmpty) {
        debugPrint('Country "$candidate" returned empty list, trying next...');
        continue;
      }

      final contentData = _parseResponse(ContentType.country, decoded);

      // Use exact name from API response for the flag request
      final exactName = decoded[0]['name'] as String? ?? candidate;

      final flagRes = await http.get(
        Uri.parse('https://api.api-ninjas.com/v1/countryflag?country=${Uri.encodeComponent(exactName)}'),
        headers: headers,
      ).timeout(const Duration(seconds: 10));

      final flagSvg = flagRes.statusCode == 200 ? flagRes.body : null;

      return ContentData(
        preview: contentData.preview,
        details: contentData.details,
        hasDetails: contentData.hasDetails,
        flagSvg: flagSvg,
      );
    }

    throw Exception('No country data available');
  }

  ContentData _parseResponse(ContentType type, dynamic decoded) {
    switch (type) {
      case ContentType.anecdote:
        if (decoded is List && decoded.isNotEmpty) {
          return ContentData(
            preview: decoded[0]['fact'] ?? 'No content',
          );
        }
        break;

      case ContentType.chuckNorris:
        if (decoded is Map) {
          return ContentData(
            preview: decoded['joke'] ?? 'No joke',
          );
        }
        break;

      case ContentType.advice:
        if (decoded is List && decoded.isNotEmpty) {
          final quote = decoded[0]['quote'] ?? '';
          final author = decoded[0]['author'] ?? 'Anonymous';
          final category = decoded[0]['category'] ?? '';
          return ContentData(
            preview: '"$quote"',
            details: '— $author\nCategory: $category',
            hasDetails: true,
          );
        }
        break;

      case ContentType.history:
        if (decoded is List && decoded.isNotEmpty) {
          final event = decoded[0];
          final year = event['year'] ?? '';
          final eventText = event['event'] ?? '';
          final now = DateTime.now();
          final monthNames = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
          final day = now.day;
          final suffix = day == 1 ? 'st' : day == 2 ? 'nd' : day == 3 ? 'rd' : 'th';
          final dateStr = '$day$suffix ${monthNames[now.month]}';
          return ContentData(
            preview: '$dateStr $year\n\n$eventText',
          );
        }
        break;

      case ContentType.country:
        if (decoded is List && decoded.isNotEmpty) {
          final c = decoded[0] as Map<String, dynamic>;
          final name = c['name'] ?? 'Unknown';
          final iso2 = (c['iso2'] as String? ?? '').toUpperCase();
          final flag = iso2.length == 2
              ? iso2.split('').map((ch) => String.fromCharCode(ch.codeUnitAt(0) - 0x41 + 0x1F1E6)).join()
              : '🌍';
          final capital = c['capital'] ?? '';
          final region = c['region'] ?? '';
          final population = c['population'];
          final area = c['surface_area'] ?? c['area'];
          final gdp = c['gdp'];
          final currency = c['currency'] as Map<String, dynamic>?;
          final languages = c['languages'] as Map<String, dynamic>?;
          final lifeExpectancy = c['life_expectancy'];
          final unemployment = c['unemployment'];

          final details = StringBuffer();
          if (capital.isNotEmpty) details.writeln('🏛️ Capital: $capital');
          if (region.isNotEmpty) details.writeln('🌐 Region: $region');
          if (population != null) {
            // L'API retourne la population en milliers → multiplier par 1000
            final pop = ((population as num) * 1000).toInt();
            final String formatted;
            if (pop >= 1000000000) {
              formatted = '${(pop / 1000000000).toStringAsFixed(1)}B';
            } else if (pop >= 1000000) {
              formatted = '${(pop / 1000000).toStringAsFixed(1)}M';
            } else if (pop >= 1000) {
              formatted = '${(pop / 1000).toStringAsFixed(0)}K';
            } else {
              formatted = '$pop';
            }
            details.writeln('👥 Population: $formatted');
          }
          if (area != null) {
            final km2 = (area as num).toInt();
            details.writeln('📐 Area: ${km2.toString().replaceAllMapped(RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), (m) => '${m[1]},')} km²');
          }
          if (gdp != null) {
            final gdpM = (gdp as num).toInt();
            details.writeln('💰 GDP: \$${(gdpM / 1000).toStringAsFixed(0)}B');
          }
          if (currency != null) {
            final cName = currency['name'] ?? '';
            final cCode = currency['code'] ?? '';
            final cSymbol = currency['symbol'] ?? '';
            details.writeln('💱 Currency: $cName ($cCode $cSymbol)'.trim());
          }
          if (languages != null && languages.isNotEmpty) {
            details.writeln('🗣️ Languages: ${languages.values.join(', ')}');
          }
          if (lifeExpectancy != null) {
            details.writeln('❤️ Life expectancy: ${lifeExpectancy.toStringAsFixed(1)} yrs');
          }
          if (unemployment != null) {
            details.writeln('📊 Unemployment: ${unemployment.toStringAsFixed(1)}%');
          }

          return ContentData(
            preview: '$flag $name',
            details: details.toString().trim(),
            hasDetails: true,
          );
        }
        break;

      case ContentType.animals:
        if (decoded is List && decoded.isNotEmpty) {
          final animal = decoded[0];
          final name = animal['name'] ?? 'Unknown';
          final taxonomy = animal['taxonomy'] as Map<String, dynamic>? ?? {};
          final characteristics = animal['characteristics'] as Map<String, dynamic>? ?? {};
          final locations = animal['locations'] as List? ?? [];

          final dayOfYear = _dayOfYear();
          final animalKeys = verifiedAnimals.keys.toList();
          final searchKey = animalKeys[dayOfYear % animalKeys.length];
          final emoji = animalEmojis[searchKey] ?? '🐾';
          final preview = '$emoji $name';

          final detailsBuffer = StringBuffer();

          if (taxonomy.isNotEmpty) {
            detailsBuffer.writeln('📚 TAXONOMY');
            if (taxonomy['kingdom'] != null) detailsBuffer.writeln('  Kingdom: ${taxonomy['kingdom']}');
            if (taxonomy['phylum'] != null) detailsBuffer.writeln('  Phylum: ${taxonomy['phylum']}');
            if (taxonomy['class'] != null) detailsBuffer.writeln('  Class: ${taxonomy['class']}');
            if (taxonomy['order'] != null) detailsBuffer.writeln('  Order: ${taxonomy['order']}');
            if (taxonomy['family'] != null) detailsBuffer.writeln('  Family: ${taxonomy['family']}');
            if (taxonomy['genus'] != null) detailsBuffer.writeln('  Genus: ${taxonomy['genus']}');
            if (taxonomy['scientific_name'] != null) detailsBuffer.writeln('  Scientific name: ${taxonomy['scientific_name']}');
            detailsBuffer.writeln('');
          }

          if (characteristics.isNotEmpty) {
            detailsBuffer.writeln('📊 CHARACTERISTICS');
            if (characteristics['lifespan'] != null) detailsBuffer.writeln('  Lifespan: ${characteristics['lifespan']}');
            if (characteristics['weight'] != null) detailsBuffer.writeln('  Weight: ${characteristics['weight']}');
            if (characteristics['height'] != null) detailsBuffer.writeln('  Height: ${characteristics['height']}');
            if (characteristics['length'] != null) detailsBuffer.writeln('  Length: ${characteristics['length']}');
            if (characteristics['top_speed'] != null) detailsBuffer.writeln('  Top speed: ${characteristics['top_speed']}');
            if (characteristics['diet'] != null) detailsBuffer.writeln('  Diet: ${characteristics['diet']}');
            if (characteristics['habitat'] != null) detailsBuffer.writeln('  Habitat: ${characteristics['habitat']}');
            if (characteristics['prey'] != null) detailsBuffer.writeln('  Prey: ${characteristics['prey']}');
            if (characteristics['predators'] != null) detailsBuffer.writeln('  Predators: ${characteristics['predators']}');
            detailsBuffer.writeln('');
          }

          if (locations.isNotEmpty) {
            detailsBuffer.writeln('📍 LOCATION');
            detailsBuffer.writeln('  ${locations.join(', ')}');
          }

          return ContentData(
            preview: preview,
            details: detailsBuffer.toString().trim(),
            hasDetails: true,
          );
        }
        break;

      case ContentType.exoplanet:
        break; // jamais atteint, géré en amont dans fetchContent
    }
    return ContentData(preview: 'Content not available');
  }
}
