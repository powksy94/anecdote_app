import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

class FavoritesGate extends StatelessWidget {
  const FavoritesGate({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  Icons.bookmark_border_rounded,
                  size: 72,
                  color: theme.colorScheme.outline,
                ),
                const SizedBox(height: 20),
                Text(
                  loc.loginRequired,
                  style: theme.textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 10),
                Text(
                  loc.loginToSaveFavorites,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: theme.colorScheme.onSurface.withValues(alpha: 0.65),
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 32),
                FilledButton(
                  onPressed: () {},
                  child: Text(loc.signIn),
                ),
                const SizedBox(height: 12),
                OutlinedButton(
                  onPressed: () {},
                  child: Text(loc.createAccount),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
