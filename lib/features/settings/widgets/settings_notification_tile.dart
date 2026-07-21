import 'package:app_settings/app_settings.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../services/notification_preference_service.dart';

class SettingsNotificationTile extends StatefulWidget {
  const SettingsNotificationTile({super.key});

  @override
  State<SettingsNotificationTile> createState() => _SettingsNotificationTileState();
}

class _SettingsNotificationTileState extends State<SettingsNotificationTile> {
  final _service = NotificationPreferenceService();
  bool _enabled = true;
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final enabled = await _service.isEnabled();
    if (!mounted) return;
    setState(() {
      _enabled = enabled;
      _loaded = true;
    });
  }

  Future<void> _onChanged(bool value) async {
    setState(() => _enabled = value);
    await _service.setEnabled(value);
    if (value) {
      await FirebaseMessaging.instance.requestPermission(
        alert: true,
        badge: true,
        sound: true,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Column(
      children: [
        SwitchListTile(
          secondary: const Icon(Icons.notifications_rounded),
          title: Text(loc.settingsNotificationsTitle),
          subtitle: Text(loc.settingsNotificationsSubtitle),
          value: _enabled,
          onChanged: _loaded ? _onChanged : null,
        ),
        if (_loaded && !_enabled)
          ListTile(
            leading: const SizedBox(width: 24),
            title: Text(
              loc.settingsOpenSystemSettings,
              style: Theme.of(context).textTheme.bodySmall,
            ),
            trailing: const Icon(Icons.open_in_new_rounded, size: 16),
            onTap: () => AppSettings.openAppSettings(
              type: AppSettingsType.notification,
            ),
          ),
      ],
    );
  }
}
