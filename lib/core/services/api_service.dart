import 'dart:convert';
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../../features/science/data/verified_animals.dart';
import '../../features/world/services/country_service.dart';
import '../../features/world/services/department_service.dart';
import '../../features/world/services/pacific_island_service.dart';
import '../../features/space/services/star_service.dart';
import '../../features/space/services/moon_service.dart';
import '../../features/space/services/mission_service.dart';
import '../../features/history/services/king_service.dart';
import '../../features/history/services/president_service.dart';
import '../../features/cinema/services/cinema_service.dart';
import '../../features/science/services/dinosaur_service.dart';
import '../../features/history/services/battle_service.dart';
import '../../features/art/services/painting_service.dart';
import '../../features/art/services/sculpture_service.dart';
import '../../features/art/services/architecture_service.dart';
import '../../features/art/services/famous_artist_service.dart';
import '../../features/art/services/photographer_service.dart';
import '../../features/art/services/classical_composer_service.dart';
import '../../features/art/services/nobel_prize_service.dart';
import '../../features/world/services/commune_service.dart';
import '../../features/world/services/state_service.dart';
import '../../features/space/services/exoplanet_service.dart';

int _dayOfYear() {
  final now = DateTime.now();
  final todayUtc = DateTime.utc(now.year, now.month, now.day);
  return todayUtc.difference(DateTime.utc(now.year, 1, 1)).inDays;
}

class ApiService {
  final String apiKey;
  ApiService({required this.apiKey});

  // ── Routing ─────────────────────────────────────────────────────────────

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
        final key = verifiedAnimals.keys.toList()[_dayOfYear() % verifiedAnimals.length];
        return 'https://api.api-ninjas.com/v1/animals?name=${Uri.encodeComponent(key)}';
      default:
        return '';
    }
  }

  // ── Dispatch ─────────────────────────────────────────────────────────────

  Future<ContentData> fetchContent(ContentType type) async {
    try {
      if (type == ContentType.exoplanet)       return await ExoplanetService().getDailyContent();
      if (type == ContentType.country)         return await CountryService().getDailyContent();
      if (type == ContentType.frenchDepartment)return await DepartmentService().getDailyContent();
      if (type == ContentType.pacificIsland)   return await PacificIslandsService().getDailyContent();
      if (type == ContentType.star)            return await StarService().getDailyContent();
      if (type == ContentType.solarSystemMoon) return await MoonService().getDailyContent();
      if (type == ContentType.spaceMission)    return await SpaceMissionService().getDailyContent();
      if (type == ContentType.kingOfFrance)    return await KingService().getDailyContent();
      if (type == ContentType.americanPresident) return await PresidentService().getDailyContent();
      if (type == ContentType.dinosaur)        return await DinosaurService().getDailyContent();
      if (type == ContentType.battle)          return await BattleService().getDailyContent();
      if (type == ContentType.painting)        return await PaintingService().getDailyContent();
      if (type == ContentType.sculpture)       return await SculptureService().getDailyContent();
      if (type == ContentType.architecture)    return await ArchitectureService().getDailyContent();
      if (type == ContentType.famousArtist)    return await FamousArtistService().getDailyContent();
      if (type == ContentType.photographer)    return await PhotographerService().getDailyContent();
      if (type == ContentType.classicalComposer) return await ClassicalComposerService().getDailyContent();
      if (type == ContentType.nobelPrize)      return await NobelPrizeService().getDailyContent();
      if (type == ContentType.frenchCommune)   return await CommuneService().getDailyContent();
      if (type == ContentType.americanState)   return await StateService().getDailyContent();
      if (type == ContentType.classicCinema ||
          type == ContentType.cinema80s90s ||
          type == ContentType.modernCinema) {
        return await CinemaService(type).getDailyContent();
      }
      if (type == ContentType.chuckNorris)     return await _fetchChuckNorrisContent();

      final response = await http.get(
        Uri.parse(_getEndpoint(type)),
        headers: {'X-Api-Key': apiKey},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode != 200) throw Exception('Server error (${response.statusCode})');
      final parsed = _parseResponse(type, jsonDecode(response.body));
      if (type == ContentType.animals) {
        final searchKey = verifiedAnimals.keys.toList()[_dayOfYear() % verifiedAnimals.length];
        final imageUrl = await _fetchWikiImage(searchKey);
        return ContentData(
          preview: parsed.preview, details: parsed.details, hasDetails: parsed.hasDetails,
          imageUrl: imageUrl,
          noImageMessage: imageUrl == null ? '🐾 No image available for this animal' : null,
        );
      }
      return parsed;
    } on http.ClientException {
      throw Exception('Network error');
    } on TimeoutException {
      throw Exception('Request timed out');
    }
  }

  // ── Chuck Norris ─────────────────────────────────────────────────────────

  static const _chuckHistoryKey = 'chuck_norris_history';
  static const _chuckHistorySize = 30;

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

    if (lastJoke == 'No joke') throw Exception('Unable to fetch Chuck Norris joke');
    history.add(lastJoke);
    if (history.length > _chuckHistorySize) history.removeAt(0);
    await prefs.setStringList(_chuckHistoryKey, history);
    return ContentData(preview: lastJoke);
  }

  // ── Parsers ──────────────────────────────────────────────────────────────

  ContentData _parseResponse(ContentType type, dynamic decoded) {
    switch (type) {
      case ContentType.anecdote:      return _parseAnecdote(decoded);
      case ContentType.chuckNorris:   return _parseChuckNorris(decoded);
      case ContentType.celebrityQuote:return _parseCelebrityQuote(decoded);
      case ContentType.history:       return _parseHistory(decoded);
      case ContentType.animals:       return _parseAnimals(decoded);
      default:                        return ContentData(preview: 'Content not available');
    }
  }

  ContentData _parseAnecdote(dynamic decoded) {
    if (decoded is List && decoded.isNotEmpty) {
      return ContentData(preview: decoded[0]['fact'] ?? 'No content');
    }
    return ContentData(preview: 'Content not available');
  }

  ContentData _parseChuckNorris(dynamic decoded) {
    if (decoded is Map) return ContentData(preview: decoded['joke'] ?? 'No joke');
    return ContentData(preview: 'Content not available');
  }

  ContentData _parseCelebrityQuote(dynamic decoded) {
    if (decoded is List && decoded.isNotEmpty) {
      return ContentData(
        preview: '"${decoded[0]['quote'] ?? ''}"',
        details: '— ${decoded[0]['author'] ?? 'Anonymous'}',
        hasDetails: true,
      );
    }
    return ContentData(preview: 'Content not available');
  }

  ContentData _parseHistory(dynamic decoded) {
    if (decoded is! List || decoded.isEmpty) return ContentData(preview: 'Content not available');
    final event   = decoded[0];
    final rawYear = event['year'] as String? ?? '';
    final yearInt = int.tryParse(rawYear);
    final String displayYear;
    if (yearInt == null) {
      displayYear = '';
    } else if (yearInt < 0) {
      displayYear = '${yearInt.abs()} BC';
    } else {
      displayYear = yearInt.toString();
    }
    final eventText = (event['event'] as String? ?? '').replaceAll(RegExp(r'\[[^\]]*\]'), '').trim();
    final now = DateTime.now();
    final months = ['','January','February','March','April','May','June','July','August','September','October','November','December'];
    final day = now.day;
    final suffix = day == 1 ? 'st' : day == 2 ? 'nd' : day == 3 ? 'rd' : 'th';
    final datePart = displayYear.isEmpty ? '$day$suffix ${months[now.month]}' : '$day$suffix ${months[now.month]} $displayYear';
    return ContentData(preview: '$datePart\n\n$eventText');
  }

  Future<String?> _fetchWikiImage(String name) async {
    try {
      final url = 'https://en.wikipedia.org/api/rest_v1/page/summary/${Uri.encodeComponent(name)}';
      final r = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 5));
      if (r.statusCode == 200) {
        return (jsonDecode(r.body) as Map<String, dynamic>)['thumbnail']?['source'] as String?;
      }
    } catch (_) {}
    return null;
  }

  ContentData _parseAnimals(dynamic decoded) {
    if (decoded is! List || decoded.isEmpty) return ContentData(preview: 'Content not available');
    final animal          = decoded[0];
    final name            = animal['name'] ?? 'Unknown';
    final taxonomy        = animal['taxonomy']        as Map<String, dynamic>? ?? {};
    final characteristics = animal['characteristics'] as Map<String, dynamic>? ?? {};
    final locations       = animal['locations']       as List? ?? [];
    final searchKey       = verifiedAnimals.keys.toList()[_dayOfYear() % verifiedAnimals.length];
    final emoji           = animalEmojis[searchKey] ?? '🐾';
    final buf = StringBuffer();
    if (taxonomy.isNotEmpty) {
      buf.writeln('📚 TAXONOMY');
      for (final k in ['kingdom','phylum','class','order','family','genus','scientific_name']) {
        if (taxonomy[k] != null) buf.writeln('  ${k == 'scientific_name' ? 'Scientific name' : k[0].toUpperCase() + k.substring(1)}: ${taxonomy[k]}');
      }
      buf.writeln('');
    }
    if (characteristics.isNotEmpty) {
      buf.writeln('📊 CHARACTERISTICS');
      for (final k in ['lifespan','weight','height','length','top_speed','diet','habitat','prey','predators']) {
        if (characteristics[k] != null) buf.writeln('  ${k[0].toUpperCase() + k.substring(1).replaceAll('_', ' ')}: ${characteristics[k]}');
      }
      buf.writeln('');
    }
    if (locations.isNotEmpty) {
      buf.writeln('📍 LOCATION');
      buf.writeln('  ${locations.join(', ')}');
    }
    return ContentData(preview: '$emoji $name', details: buf.toString().trim(), hasDetails: true);
  }
}
