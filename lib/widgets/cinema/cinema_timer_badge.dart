import 'package:flutter/material.dart';
import '../../generated/app_localizations.dart';

class CinemaTimerBadge extends StatelessWidget {
  final String timeUntilMidnight;
  final Color accentColor;

  const CinemaTimerBadge({
    super.key,
    required this.timeUntilMidnight,
    required this.accentColor,
  });

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.schedule_rounded, size: 16, color: accentColor),
          const SizedBox(width: 8),
          Text(
            loc.newContentIn(timeUntilMidnight),
            style: TextStyle(
              fontSize: 13,
              color: accentColor,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}
