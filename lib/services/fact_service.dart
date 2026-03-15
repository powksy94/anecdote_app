import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/fact.dart';
import 'dart:async';

class FactService {
  final String apiKey;

  FactService({required this.apiKey});

  Future<Fact> fetchFactOfTheDay() async {
    const url = 'https://api.api-ninjas.com/v1/factoftheday';

    try {
      final response = await http.get(
        Uri.parse(url),
        headers: {'X-Api-Key': apiKey},
      ).timeout(const Duration(seconds: 5));

      if (response.statusCode != 200) {
        throw Exception('Server error (${response.statusCode})');
      }

      final decoded = jsonDecode(response.body);

      if (decoded is! List || decoded.isEmpty) {
        throw Exception('Invalid API response');
      }

      return Fact.fromJson(decoded[0]);
    } catch (e) {
      if (e is http.ClientException) {
        throw Exception('Network error: ${e.message}');
      } else if (e is FormatException) {
        throw Exception('JSON parsing error: ${e.message}');
      } else if (e is TimeoutException) {
        throw Exception('Request timed out');
      } else {
        throw Exception('Unexpected error: $e');
      }
    }
  }
}
