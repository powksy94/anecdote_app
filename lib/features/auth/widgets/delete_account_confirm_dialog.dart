import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

Future<bool> showDeleteAccountConfirmDialog(BuildContext context) async {
  final loc = AppLocalizations.of(context)!;
  final confirmed = await showDialog<bool>(
    context: context,
    builder: (ctx) => AlertDialog(
      title: Text(loc.deleteAccountConfirmTitle),
      content: Text(loc.deleteAccountConfirmMessage),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(ctx, false),
          child: Text(loc.cancelButton),
        ),
        TextButton(
          onPressed: () => Navigator.pop(ctx, true),
          child: Text(
            loc.deleteAccountConfirmButton,
            style: TextStyle(color: Theme.of(ctx).colorScheme.error),
          ),
        ),
      ],
    ),
  );
  return confirmed ?? false;
}
