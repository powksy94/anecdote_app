import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../widgets/settings_notification_tile.dart';
import '../widgets/settings_sound_tile.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(title: Text(loc.settingsTitle)),
      body: const Column(
        children: [
          SettingsSoundTile(),
          Divider(height: 1),
          SettingsNotificationTile(),
        ],
      ),
    );
  }
}
