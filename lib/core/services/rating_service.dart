import 'package:in_app_review/in_app_review.dart';
import 'package:shared_preferences/shared_preferences.dart';

class RatingService {
  static const _keyOpenCount = 'app_open_count';
  static const _keyLastShown = 'rating_last_shown';
  static const _minOpens = 5;
  static const _minDaysBetweenPrompts = 30;

  Future<void> recordOpen() async {
    final prefs = await SharedPreferences.getInstance();
    final count = prefs.getInt(_keyOpenCount) ?? 0;
    await prefs.setInt(_keyOpenCount, count + 1);
  }

  Future<bool> shouldPrompt() async {
    final prefs = await SharedPreferences.getInstance();
    final count = prefs.getInt(_keyOpenCount) ?? 0;
    if (count < _minOpens) return false;

    final lastShown = prefs.getString(_keyLastShown);
    if (lastShown != null) {
      final last = DateTime.tryParse(lastShown);
      if (last != null) {
        final daysSince = DateTime.now().difference(last).inDays;
        if (daysSince < _minDaysBetweenPrompts) return false;
      }
    }

    final inAppReview = InAppReview.instance;
    return inAppReview.isAvailable();
  }

  Future<void> markShown() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyLastShown, DateTime.now().toIso8601String().substring(0, 10));
  }

  Future<void> requestReview() async {
    await InAppReview.instance.requestReview();
  }
}
