import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../widgets/settings_notification_tile.dart';
import '../widgets/settings_sound_tile.dart';
import '../widgets/settings_terms_footer.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(title: Text(loc.settingsTitle)),
      // Scrollable so small screens, landscape or large fonts can't overflow; the footer
      // still sits at the bottom whenever there is spare height.
      body: const CustomScrollView(
        slivers: [
          SliverToBoxAdapter(child: SettingsSoundTile()),
          SliverToBoxAdapter(child: Divider(height: 1)),
          SliverToBoxAdapter(child: SettingsNotificationTile()),
          SliverFillRemaining(
            hasScrollBody: false,
            child: Align(
              alignment: Alignment.bottomCenter,
              child: SettingsTermsFooter(),
            ),
          ),
        ],
      ),
    );
  }
}
