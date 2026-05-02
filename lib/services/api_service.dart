import 'dart:convert';
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../data/verified_animals.dart';
import 'world_service/country_service.dart';
import 'world_service/department_service.dart';
import 'world_service/pacific_island_service.dart';
import 'exoplanet_service.dart';

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
      case ContentType.celebrityQuote:
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
      case ContentType.frenchDepartment:
      case ContentType.pacificIsland:
      case ContentType.world:
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
        return await CountryService().getDailyContent();
      }
      if (type == ContentType.frenchDepartment) {
        return await DepartmentService().getDailyContent();
      }
      if (type == ContentType.pacificIsland) {
        return await PacificIslandsService().getDailyContent();
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

    if (lastJoke == 'No joke') {
      throw Exception('Unable to fetch Chuck Norris joke');
    }

    history.add(lastJoke);
    if (history.length > _chuckHistorySize) history.removeAt(0);
    await prefs.setStringList(_chuckHistoryKey, history);

    return ContentData(preview: lastJoke);
  }

  ContentData _parseResponse(ContentType type, dynamic decoded) {
    switch (type) {
      case ContentType.anecdote:
        if (decoded is List && decoded.isNotEmpty) {
          return ContentData(preview: decoded[0]['fact'] ?? 'No content');
        }
        break;

      case ContentType.chuckNorris:
        if (decoded is Map) {
          return ContentData(preview: decoded['joke'] ?? 'No joke');
        }
        break;

      case ContentType.celebrityQuote:
        if (decoded is List && decoded.isNotEmpty) {
          final quote  = decoded[0]['quote']  ?? '';
          final author = decoded[0]['author'] ?? 'Anonymous';
          return ContentData(
            preview: '"$quote"',
            details: '— $author',
            hasDetails: true,
          );
        }
        break;

      case ContentType.history:
        if (decoded is List && decoded.isNotEmpty) {
          final event    = decoded[0];
          final rawYear  = event['year'] as String? ?? '';
          final yearInt  = int.tryParse(rawYear) ?? 0;
          final displayYear = yearInt < 0 ? '${yearInt.abs()} BC' : rawYear;
          final eventText = (event['event'] as String? ?? '')
              .replaceAll(RegExp(r'\[[^\]]*\]'), '')
              .trim();
          final now = DateTime.now();
          final monthNames = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
          final day    = now.day;
          final suffix = day == 1 ? 'st' : day == 2 ? 'nd' : day == 3 ? 'rd' : 'th';
          return ContentData(
            preview: '$day$suffix ${monthNames[now.month]} $displayYear\n\n$eventText',
          );
        }
        break;

      case ContentType.animals:
        if (decoded is List && decoded.isNotEmpty) {
          final animal         = decoded[0];
          final name           = animal['name'] ?? 'Unknown';
          final taxonomy       = animal['taxonomy']       as Map<String, dynamic>? ?? {};
          final characteristics = animal['characteristics'] as Map<String, dynamic>? ?? {};
          final locations      = animal['locations']      as List? ?? [];

          final dayOfYear  = _dayOfYear();
          final animalKeys = verifiedAnimals.keys.toList();
          final searchKey  = animalKeys[dayOfYear % animalKeys.length];
          final emoji      = animalEmojis[searchKey] ?? '🐾';

          final buf = StringBuffer();
          if (taxonomy.isNotEmpty) {
            buf.writeln('📚 TAXONOMY');
            if (taxonomy['kingdom']       != null) buf.writeln('  Kingdom: ${taxonomy['kingdom']}');
            if (taxonomy['phylum']        != null) buf.writeln('  Phylum: ${taxonomy['phylum']}');
            if (taxonomy['class']         != null) buf.writeln('  Class: ${taxonomy['class']}');
            if (taxonomy['order']         != null) buf.writeln('  Order: ${taxonomy['order']}');
            if (taxonomy['family']        != null) buf.writeln('  Family: ${taxonomy['family']}');
            if (taxonomy['genus']         != null) buf.writeln('  Genus: ${taxonomy['genus']}');
            if (taxonomy['scientific_name'] != null) buf.writeln('  Scientific name: ${taxonomy['scientific_name']}');
            buf.writeln('');
          }
          if (characteristics.isNotEmpty) {
            buf.writeln('📊 CHARACTERISTICS');
            if (characteristics['lifespan']  != null) buf.writeln('  Lifespan: ${characteristics['lifespan']}');
            if (characteristics['weight']    != null) buf.writeln('  Weight: ${characteristics['weight']}');
            if (characteristics['height']    != null) buf.writeln('  Height: ${characteristics['height']}');
            if (characteristics['length']    != null) buf.writeln('  Length: ${characteristics['length']}');
            if (characteristics['top_speed'] != null) buf.writeln('  Top speed: ${characteristics['top_speed']}');
            if (characteristics['diet']      != null) buf.writeln('  Diet: ${characteristics['diet']}');
            if (characteristics['habitat']   != null) buf.writeln('  Habitat: ${characteristics['habitat']}');
            if (characteristics['prey']      != null) buf.writeln('  Prey: ${characteristics['prey']}');
            if (characteristics['predators'] != null) buf.writeln('  Predators: ${characteristics['predators']}');
            buf.writeln('');
          }
          if (locations.isNotEmpty) {
            buf.writeln('📍 LOCATION');
            buf.writeln('  ${locations.join(', ')}');
          }

          return ContentData(
            preview: '$emoji $name',
            details: buf.toString().trim(),
            hasDetails: true,
          );
        }
        break;

      case ContentType.country:
      case ContentType.frenchDepartment:
      case ContentType.pacificIsland:
      case ContentType.world:
      case ContentType.exoplanet:
        break;
    }
    return ContentData(preview: 'Content not available');
  }
}
