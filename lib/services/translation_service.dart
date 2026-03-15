import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/content_data.dart';

class TranslationService {
  final String apiKey;

  TranslationService({required this.apiKey});

  static const String _endpoint =
      'https://translation.googleapis.com/language/translate/v2';

  Future<String> _translateText(String text, String targetLang) async {
    final response = await http.post(
      Uri.parse('$_endpoint?key=$apiKey'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'q': text,
        'source': 'en',
        'target': targetLang,
        'format': 'text',
      }),
    ).timeout(const Duration(seconds: 10));

    if (response.statusCode != 200) {
      throw Exception('Translation error (${response.statusCode})');
    }

    final data = jsonDecode(response.body);
    return data['data']['translations'][0]['translatedText'] as String;
  }

  Future<ContentData> translateContent(
    ContentData content, {
    required String targetLang,
  }) async {
    if (targetLang == 'en') return content;

    final translatedPreview = await _translateText(content.preview, targetLang);

    String translatedDetails = content.details;
    if (content.hasDetails && content.details.isNotEmpty) {
      translatedDetails = await _translateText(content.details, targetLang);
    }

    return ContentData(
      preview: translatedPreview,
      details: translatedDetails,
      hasDetails: content.hasDetails,
    );
  }
}
