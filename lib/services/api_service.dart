import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../data/verified_animals.dart';

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
        final dayOfYear = DateTime.now().difference(DateTime(DateTime.now().year, 1, 1)).inDays;
        final animalKeys = verifiedAnimals.keys.toList();
        final selectedAnimal = animalKeys[dayOfYear % animalKeys.length];
        return 'https://api.api-ninjas.com/v1/animals?name=${Uri.encodeComponent(selectedAnimal)}';
    }
  }

  Future<ContentData> fetchContent(ContentType type) async {
    try {
      final response = await http.get(
        Uri.parse(_getEndpoint(type)),
        headers: {'X-Api-Key': apiKey},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode != 200) {
        throw Exception('Server error (${response.statusCode})');
      }

      final decoded = jsonDecode(response.body);
      return _parseResponse(type, decoded);
    } catch (e) {
      if (e is http.ClientException) {
        throw Exception('Network error');
      } else if (e is TimeoutException) {
        throw Exception('Request timed out');
      } else {
        throw Exception('$e');
      }
    }
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

      case ContentType.animals:
        if (decoded is List && decoded.isNotEmpty) {
          final animal = decoded[0];
          final name = animal['name'] ?? 'Unknown';
          final taxonomy = animal['taxonomy'] as Map<String, dynamic>? ?? {};
          final characteristics = animal['characteristics'] as Map<String, dynamic>? ?? {};
          final locations = animal['locations'] as List? ?? [];

          final dayOfYear = DateTime.now().difference(DateTime(DateTime.now().year, 1, 1)).inDays;
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
    }
    return ContentData(preview: 'Content not available');
  }
}
