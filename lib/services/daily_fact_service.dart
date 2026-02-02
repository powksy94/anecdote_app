import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class DailyFactCache {
  static const _key = 'daily_fact';

  Future<Map<String, dynamic>?> getTodayFact() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_key);
    if (raw == null) return null;

    final data = jsonDecode(raw);
    final savedDate = DateTime.parse(data['date']);
    final today = DateTime.now();

    if (savedDate.year == today.year &&
        savedDate.month == today.month &&
        savedDate.day == today.day) {
      return data;
    }

    return null;
  }

  Future<void> saveTodayFact({
    required String original,
    String? translated,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    final data = {
      'date': DateTime.now().toIso8601String(),
      'original': original,
      'translated': translated,
    };

    await prefs.setString(_key, jsonEncode(data));
  }

  Future<void> clearCache() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_key);
  }
}
