import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import '../models/content_type.dart';
import '../models/content_data.dart';

class DailyCacheService {
  String _keyFor(ContentType type, {String locale = 'en'}) =>
      'daily_${type.name}_$locale';

  Future<ContentData?> getTodayContent(ContentType type,
      {String locale = 'en'}) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_keyFor(type, locale: locale));
    if (raw == null) return null;

    try {
      final data = jsonDecode(raw);
      final savedDate = DateTime.parse(data['date']);
      final today = DateTime.now();

      if (savedDate.year == today.year &&
          savedDate.month == today.month &&
          savedDate.day == today.day) {
        return ContentData(
          preview: data['preview'] ?? '',
          details: data['details'] ?? '',
          hasDetails: data['hasDetails'] ?? false,
        );
      }
      return null;
    } catch (e) {
      await clearCache(type);
      return null;
    }
  }

  Future<void> saveTodayContent(ContentType type, ContentData content,
      {String locale = 'en'}) async {
    final prefs = await SharedPreferences.getInstance();
    final data = {
      'date': DateTime.now().toIso8601String(),
      'preview': content.preview,
      'details': content.details,
      'hasDetails': content.hasDetails,
    };
    await prefs.setString(_keyFor(type, locale: locale), jsonEncode(data));
  }

  Future<void> clearCache(ContentType type, {String? locale}) async {
    final prefs = await SharedPreferences.getInstance();
    if (locale != null) {
      await prefs.remove(_keyFor(type, locale: locale));
    } else {
      for (final loc in ['en', 'fr', 'es']) {
        await prefs.remove(_keyFor(type, locale: loc));
      }
    }
  }

  Future<void> clearAllCache() async {
    final prefs = await SharedPreferences.getInstance();
    for (final type in ContentType.values) {
      for (final locale in ['en', 'fr', 'es']) {
        await prefs.remove(_keyFor(type, locale: locale));
      }
    }
  }
}
