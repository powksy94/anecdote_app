import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/fact.dart';

class FactService {
  final String apiKey;

  FactService({required this.apiKey});

  Future<Fact> fetchFactOfTheDay() async {
    const url = 'https://api.api-ninjas.com/v1/factoftheday';
    final response = await http.get(
      Uri.parse(url),
      headers: {'X-Api-Key': apiKey},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return Fact.fromJson(data[0]);
    } else {
      throw Exception('Impossible de récupérer la donnée.');
    }
  }
}
