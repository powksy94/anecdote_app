import 'package:flutter/foundation.dart';
import 'package:in_app_update/in_app_update.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum VersionCheckResult { noUpdate, updateAvailable, justUpdated }

class VersionCheckService {
  static const _keyJustUpdated = 'just_updated';
  static const _keyLastCheckDate = 'version_last_check_date';
  static const _keySnoozeUntil = 'update_snooze_until';
  static const bool _debugForceUpdate = false;

  Future<VersionCheckResult> check() async {
    final prefs = await SharedPreferences.getInstance();

    final justUpdated = prefs.getBool(_keyJustUpdated) ?? false;
    if (justUpdated) {
      await prefs.setBool(_keyJustUpdated, false);
      return VersionCheckResult.justUpdated;
    }

    if (kDebugMode) {
      return _debugForceUpdate
          ? VersionCheckResult.updateAvailable
          : VersionCheckResult.noUpdate;
    }

    // Snoozé par l'utilisateur ?
    if (await _isSnoozed(prefs)) return VersionCheckResult.noUpdate;

    // Ne vérifier qu'une fois par jour
    final today = DateTime.now().toIso8601String().substring(0, 10);
    final lastCheck = prefs.getString(_keyLastCheckDate) ?? '';
    if (lastCheck == today) {
      return VersionCheckResult.noUpdate;
    }

    try {
      final info = await InAppUpdate.checkForUpdate();
      await prefs.setString(_keyLastCheckDate, today);
      return info.updateAvailability == UpdateAvailability.updateAvailable
          ? VersionCheckResult.updateAvailable
          : VersionCheckResult.noUpdate;
    } catch (_) {
      return VersionCheckResult.noUpdate;
    }
  }

  static Future<bool> _isSnoozed(SharedPreferences prefs) async {
    final raw = prefs.getString(_keySnoozeUntil);
    if (raw == null) return false;
    final until = DateTime.tryParse(raw);
    if (until == null) return false;
    return DateTime.now().isBefore(until);
  }

  static Future<void> snoozeUpdate() async {
    final prefs = await SharedPreferences.getInstance();
    final until = DateTime.now().add(const Duration(days: 3));
    await prefs.setString(_keySnoozeUntil, until.toIso8601String().substring(0, 10));
  }

  static Future<void> markJustUpdated() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_keyJustUpdated, true);
  }
}
