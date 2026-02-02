import 'dart:convert';
import 'package:http/http.dart' as http;

class TranslateService {
  final String targetLang;

  TranslateService({this.targetLang = 'fr'});

  Future<String> translate(String text) async {
    final response = await http.post(
      Uri.parse('https://libretranslate.com/translate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'q': text,
        'source': 'en',
        'target': targetLang,
        'format': 'text',
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['translatedText'];
    } else {
      throw Exception('Erreur traduction');
    }
  }
}
