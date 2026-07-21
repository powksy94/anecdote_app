import 'package:flutter_test/flutter_test.dart';
import 'package:projet_app_annecdote/features/settings/services/sound_preference_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  group('SoundPreferenceService', () {
    test('defaults to enabled when never set', () async {
      final result = await SoundPreferenceService().isEnabled();
      expect(result, isTrue);
    });

    test('persists a disabled preference', () async {
      final service = SoundPreferenceService();
      await service.setEnabled(false);
      expect(await service.isEnabled(), isFalse);
    });

    test('persists a re-enabled preference', () async {
      final service = SoundPreferenceService();
      await service.setEnabled(false);
      await service.setEnabled(true);
      expect(await service.isEnabled(), isTrue);
    });
  });
}
