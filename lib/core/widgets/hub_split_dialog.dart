import 'package:flutter/material.dart';
import '../models/content_type.dart';
import '../../generated/app_localizations.dart';
import 'hub_section_card.dart';

class HubSplitDialog extends StatelessWidget {
  final ContentType hubType;
  final ContentType leftType;
  final ContentType rightType;
  final VoidCallback onSelectLeft;
  final VoidCallback onSelectRight;

  const HubSplitDialog({
    super.key,
    required this.hubType,
    required this.leftType,
    required this.rightType,
    required this.onSelectLeft,
    required this.onSelectRight,
  });

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final theme = Theme.of(context);

    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      title: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(hubType.icon, size: 20, color: theme.colorScheme.primary),
          const SizedBox(width: 8),
          Text(hubType.localizedTitle(loc)),
        ],
      ),
      contentPadding: const EdgeInsets.fromLTRB(16, 12, 16, 16),
      content: IntrinsicHeight(
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(
              child: HubSectionCard(
                type: leftType,
                loc: loc,
                onTap: onSelectLeft,
              ),
            ),
            VerticalDivider(
              width: 20,
              thickness: 1.5,
              color: theme.colorScheme.onSurface.withValues(alpha: 0.15),
            ),
            Expanded(
              child: HubSectionCard(
                type: rightType,
                loc: loc,
                onTap: onSelectRight,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
