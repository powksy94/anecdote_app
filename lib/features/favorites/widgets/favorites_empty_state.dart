import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

class FavoritesEmptyState extends StatelessWidget {
  const FavoritesEmptyState({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.bookmark_border_rounded,
              size: 64, color: theme.colorScheme.outlineVariant),
          const SizedBox(height: 16),
          Text(
            loc.favoritesEmpty,
            style: theme.textTheme.bodyLarge
                ?.copyWith(color: theme.colorScheme.outline),
          ),
        ],
      ),
    );
  }
}
