import 'package:flutter/material.dart';
import '../services/preferences_service.dart';

class LanguageSelectionPage extends StatelessWidget {
  final void Function(Locale locale) onLanguageSelected;

  const LanguageSelectionPage({super.key, required this.onLanguageSelected});

  Future<void> _selectLanguage(String lang) async {
    final prefs = PreferencesService();
    await prefs.saveLanguagePreference(lang);
    onLanguageSelected(Locale(lang));
  }

    Widget _languageButton({
    required String emoji,
    required String label,
    required VoidCallback onTap,
    }) {
    return StatefulBuilder(
        builder: (context, setState) {
        bool pressed = false;

        return GestureDetector(
            onTapDown: (_) => setState(() => pressed = true),
            onTapUp: (_) {
            setState(() => pressed = false);
            onTap();
            },
            onTapCancel: () => setState(() => pressed = false),
            child: AnimatedScale(
            scale: pressed ? 0.95 : 1.0,
            duration: const Duration(milliseconds: 120),
            curve: Curves.easeOut,
            child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(18),
                ),
                child: Column(
                children: [
                    Text(emoji, style: const TextStyle(fontSize: 32)),
                    const SizedBox(height: 6),
                    Text(label, style: const TextStyle(fontSize: 16)),
                ],
                ),
            ),
            ),
        );
        },
    );
    }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Choose your language',
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 32),

            _languageButton(
              emoji: '🇬🇧',
              label: 'English',
              onTap: () => _selectLanguage('en'),
            ),

            const SizedBox(height: 16),

            _languageButton(
              emoji: '🇫🇷',
              label: 'Français',
              onTap: () => _selectLanguage('fr'),
            ),
          ],
        ),
      ),
    );
  }
}
