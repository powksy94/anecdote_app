import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

class RegisterStepCategories extends StatelessWidget {
  final Set<String> selected;
  final void Function(String id) onToggle;
  final bool loading;
  final VoidCallback onCreateAccount;

  const RegisterStepCategories({
    super.key,
    required this.selected,
    required this.onToggle,
    required this.loading,
    required this.onCreateAccount,
  });

  static List<(String, String Function(AppLocalizations), String)> get _defs => [
    ('😄', (l) => l.catAnecdote,     'anecdote'),
    ('🎬', (l) => l.catCinema,       'cinema'),
    ('⭐', (l) => l.catCelebrities,  'celebrities'),
    ('📜', (l) => l.catHistory,      'history'),
    ('🔬', (l) => l.catScience,      'science'),
    ('🎨', (l) => l.catArt,          'art'),
    ('🌍', (l) => l.catWorld,        'world'),
    ('🚀', (l) => l.catSpace,        'space'),
    ('🎮', (l) => l.catGaming,       'gaming'),
    ('🐾', (l) => l.catAnimals,      'animals'),
    ('🌋', (l) => l.catVolcano,      'volcano'),
    ('🦕', (l) => l.catDinosaur,     'dinosaur'),
    ('🏛️', (l) => l.catArchitecture, 'architecture'),
    ('🎵', (l) => l.catMusic,        'music'),
    ('💎', (l) => l.catMineral,      'mineral'),
    ('🐦', (l) => l.catBirds,        'birds'),
    ('☁️', (l) => l.catCloud,        'cloud'),
    ('🦋', (l) => l.catInsects,      'insects'),
  ];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(loc.registerStep3Title,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text(loc.registerStep3Subtitle,
              style: TextStyle(color: theme.colorScheme.outline)),
          const SizedBox(height: 24),
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: _defs.map((def) {
              final (emoji, labelFn, id) = def;
              final isSelected = selected.contains(id);
              return FilterChip(
                label: Text('$emoji ${labelFn(loc)}'),
                selected: isSelected,
                onSelected: (_) => onToggle(id),
                selectedColor: theme.colorScheme.primaryContainer,
                checkmarkColor: theme.colorScheme.primary,
              );
            }).toList(),
          ),
          const SizedBox(height: 12),
          Text(
            loc.themesSelectedCount(selected.length),
            style: TextStyle(
              color: selected.length >= 3
                  ? theme.colorScheme.primary
                  : theme.colorScheme.outline,
              fontSize: 13,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: loading ? null : onCreateAccount,
            child: loading
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(
                        strokeWidth: 2, color: Colors.white))
                : Text(loc.createAccount),
          ),
        ],
      ),
    );
  }
}
