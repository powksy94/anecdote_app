import 'package:flutter/material.dart';
import '../pages/settings_page.dart';

class SettingsIconButton extends StatelessWidget {
  const SettingsIconButton({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return IconButton(
      icon: Icon(Icons.settings_outlined, color: theme.colorScheme.primary),
      onPressed: () => Navigator.of(context, rootNavigator: true).push(
        MaterialPageRoute(builder: (_) => const SettingsPage()),
      ),
    );
  }
}
