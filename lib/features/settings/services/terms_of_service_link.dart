import 'package:url_launcher/url_launcher.dart';

abstract class TermsOfServiceLink {
  static const _supportedLangs = {'en', 'fr', 'es'};

  static Uri uriFor(String languageCode) {
    final lang = _supportedLangs.contains(languageCode) ? languageCode : 'en';
    return Uri.parse('https://powksy.com/daily-facts/terms-of-service?lang=$lang');
  }

  static Future<void> open(String languageCode) async {
    await launchUrl(uriFor(languageCode), mode: LaunchMode.externalApplication);
  }
}
