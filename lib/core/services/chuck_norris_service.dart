import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/content_data.dart';

class ChuckNorrisService {
  final String apiKey;
  ChuckNorrisService({required this.apiKey});

  static const _historyKey  = 'chuck_norris_history';
  static const _historySize = 30;

  Future<ContentData> getDailyContent() async {
    final prefs   = await SharedPreferences.getInstance();
    final history = prefs.getStringList(_historyKey) ?? [];
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
    if (history.length > _historySize) history.removeAt(0);
    await prefs.setStringList(_historyKey, history);
    return ContentData(preview: lastJoke);
  }
}
