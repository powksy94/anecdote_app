import 'package:flutter/foundation.dart';
import 'package:in_app_update/in_app_update.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum VersionCheckResult { noUpdate, updateAvailable, justUpdated }

class VersionCheckService {
  static const _keyJustUpdated = 'just_updated';
  static const bool _debugForceUpdate = true;

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

    try {
      final info = await InAppUpdate.checkForUpdate();
      return info.updateAvailability == UpdateAvailability.updateAvailable
          ? VersionCheckResult.updateAvailable
          : VersionCheckResult.noUpdate;
    } catch (_) {
      return VersionCheckResult.noUpdate;
    }
  }

  static Future<void> markJustUpdated() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_keyJustUpdated, true);
  }
}
