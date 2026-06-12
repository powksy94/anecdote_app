import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../../features/science/data/verified_animals.dart';
import 'chuck_norris_service.dart';
import 'api_response_parsers.dart';

class ApiService {
  final String apiKey;
  ApiService({required this.apiKey});

  Future<ContentData> fetchRemoteContent(ContentType type) async {
    try {
      if (type == ContentType.chuckNorris) {
        return await ChuckNorrisService(apiKey: apiKey).getDailyContent();
      }

      final response = await http.get(
        Uri.parse(_endpoint(type)),
        headers: {'X-Api-Key': apiKey},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode != 200) throw Exception('Server error (${response.statusCode})');
      final parsed = parseApiResponse(type, jsonDecode(response.body));

      if (type == ContentType.animals) {
        final searchKey = verifiedAnimals.keys.toList()[dayOfYear() % verifiedAnimals.length];
        final imageUrl  = await fetchWikiImage(searchKey);
        return ContentData(
          preview: parsed.preview,
          details: parsed.details,
          hasDetails: parsed.hasDetails,
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

  String _endpoint(ContentType type) {
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
        final key = verifiedAnimals.keys.toList()[dayOfYear() % verifiedAnimals.length];
        return 'https://api.api-ninjas.com/v1/animals?name=${Uri.encodeComponent(key)}';
      default:
        return '';
    }
  }
}
