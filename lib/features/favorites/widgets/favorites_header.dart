import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

class FavoritesHeader extends StatelessWidget {
  final String monthLabel;
  final int count;

  const FavoritesHeader({
    super.key,
    required this.monthLabel,
    required this.count,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            loc.favoritesTitle,
            style: theme.textTheme.headlineSmall
                ?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 4),
          Text(
            loc.favoritesMonth(monthLabel),
            style: theme.textTheme.bodyMedium
                ?.copyWith(color: theme.colorScheme.outline),
          ),
        ],
      ),
    );
  }
}
