import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/models/content_type.dart';
import '../../../generated/app_localizations.dart';
import '../models/favorite_fact.dart';

class FavoriteDetailSheet extends StatelessWidget {
  final FavoriteFact fact;

  const FavoriteDetailSheet({super.key, required this.fact});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;
    final gradient = fact.contentType.gradient;
    final locale = Localizations.localeOf(context).languageCode;
    final savedDate = DateFormat.yMMMMd(locale).format(fact.savedAt);

    return DraggableScrollableSheet(
      expand: false,
      initialChildSize: 0.6,
      minChildSize: 0.3,
      maxChildSize: 0.9,
      builder: (context, scrollController) => Container(
        decoration: BoxDecoration(
          color: theme.colorScheme.surface,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          children: [
            _DetailSheetHeader(fact: fact, gradient: gradient, loc: loc),
            Expanded(
              child: SingleChildScrollView(
                controller: scrollController,
                padding: const EdgeInsets.all(24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (fact.details.isNotEmpty) ...[
                      Text(
                        fact.preview,
                        style: theme.textTheme.titleLarge
                            ?.copyWith(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 12),
                      SelectableText(
                        fact.details,
                        style: theme.textTheme.bodyLarge,
                      ),
                    ] else
                      SelectableText(
                        fact.preview,
                        style: theme.textTheme.bodyLarge,
                      ),
                    const SizedBox(height: 20),
                    Text(
                      loc.favoriteSavedOn(savedDate),
                      style: theme.textTheme.bodySmall
                          ?.copyWith(color: theme.colorScheme.outline),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _DetailSheetHeader extends StatelessWidget {
  final FavoriteFact fact;
  final List<Color> gradient;
  final AppLocalizations loc;

  const _DetailSheetHeader({
    required this.fact,
    required this.gradient,
    required this.loc,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: gradient,
        ),
      ),
      child: Column(
        children: [
          Container(
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.7),
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(fact.contentType.icon, color: Colors.white, size: 20),
              const SizedBox(width: 8),
              Flexible(
                child: Text(
                  fact.contentType.localizedTitle(loc),
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
