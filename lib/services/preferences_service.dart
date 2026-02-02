// lib/services/preferences_service.dart
import 'package:shared_preferences/shared_preferences.dart';

class PreferencesService {
  static const _keyLanguage = 'language';

  Future<String> getLanguagePreference() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyLanguage) ?? 'en';
  }

  Future<void> saveLanguagePreference(String lang) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyLanguage, lang);
  }
}
