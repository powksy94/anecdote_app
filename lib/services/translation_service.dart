import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/content_data.dart';

class TranslationService {
  final String apiKey;

  TranslationService({required this.apiKey});

  static const String _endpoint =
      'https://translation.googleapis.com/language/translate/v2';

  // Correspond aux emojis des plages Unicode courantes
  static final _emojiRegex = RegExp(
    r'[\u{1F000}-\u{1FAFF}][\u{FE0F}\u{20E3}]?|'
    r'[\u{2000}-\u{2BFF}][\u{FE0F}]?',
    unicode: true,
  );

  /// Remplace chaque emoji par [E0], [E1]... et stocke les emojis dans [out].
  static String _maskEmojis(String text, List<String> out) {
    out.clear();
    return text.replaceAllMapped(_emojiRegex, (m) {
      out.add(m.group(0)!);
      return '[E${out.length - 1}]';
    });
  }

  /// Restaure les emojis depuis les placeholders [E0], [E1]...
  static String _restoreEmojis(String masked, List<String> emojis) {
    return masked.replaceAllMapped(
      RegExp(r'\[E(\d+)\]'),
      (m) {
        final idx = int.tryParse(m.group(1) ?? '') ?? -1;
        return (idx >= 0 && idx < emojis.length) ? emojis[idx] : m.group(0)!;
      },
    );
  }

  Future<String> _translateText(String text, String targetLang) async {
    final emojis = <String>[];
    final masked = _maskEmojis(text, emojis);

    final response = await http.post(
      Uri.parse('$_endpoint?key=$apiKey'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'q': masked,
        'source': 'en',
        'target': targetLang,
        'format': 'text',
      }),
    ).timeout(const Duration(seconds: 10));

    if (response.statusCode != 200) {
      throw Exception('Translation error (${response.statusCode})');
    }

    final data = jsonDecode(response.body);
    final translated = data['data']['translations'][0]['translatedText'] as String;
    return _restoreEmojis(translated, emojis);
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
