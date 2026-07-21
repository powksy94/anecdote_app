import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../services/sound_preference_service.dart';

class SettingsSoundTile extends StatefulWidget {
  const SettingsSoundTile({super.key});

  @override
  State<SettingsSoundTile> createState() => _SettingsSoundTileState();
}

class _SettingsSoundTileState extends State<SettingsSoundTile> {
  final _service = SoundPreferenceService();
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
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return SwitchListTile(
      secondary: const Icon(Icons.volume_up_rounded),
      title: Text(loc.settingsSoundTitle),
      subtitle: Text(loc.settingsSoundSubtitle),
      value: _enabled,
      onChanged: _loaded ? _onChanged : null,
    );
  }
}
