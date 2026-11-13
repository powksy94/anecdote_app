import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../services/terms_of_service_link.dart';

class SettingsTermsFooter extends StatelessWidget {
  const SettingsTermsFooter({super.key});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final lang = Localizations.localeOf(context).languageCode;
    // SafeArea keeps the link above Android's gesture bar / navigation buttons.
    return SafeArea(
      top: false,
      minimum: const EdgeInsets.only(bottom: 16),
      child: Center(
        child: TextButton(
          onPressed: () => TermsOfServiceLink.open(lang),
          child: Text(
            loc.settingsTermsOfService,
            style: const TextStyle(decoration: TextDecoration.underline),
          ),
        ),
      ),
    );
  }
}
