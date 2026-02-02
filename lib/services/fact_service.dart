import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/fact.dart';

class FactService {
  final String apiKey;

  FactService({required this.apiKey});

  Future<Fact> fetchFactOfTheDay() async {
    const url = 'https://api.api-ninjas.com/v1/factoftheday';

    try {
      final response = await http.get(
        Uri.parse(url),
        headers: {'X-Api-Key': apiKey},
      )
      .timeout(const Duration(seconds: 5));

      if (response.statusCode != 200) {
        throw Exception('Erreur serveur (${response.statusCode})');
      }

      final decoded = jsonDecode(response.body);

      if (decoded is! List || decoded.isEmpty) {
        throw Exception('Réponse API invalide');
      }

      return Fact.fromJson(decoded[0]);
   } catch (e) {
      if (e is http.ClientException) {
        throw Exception('Erreur réseau : $e');
      } else if (e is FormatException) {
        throw Exception('Erreur parsing JSON : $e');
      } else {
        throw Exception('Erreur inattendue : $e');
      }
    }

  }
}
