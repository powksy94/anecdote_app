import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

Future<String?> showReauthPasswordDialog(BuildContext context) {
  final loc = AppLocalizations.of(context)!;
  final controller = TextEditingController();
  return showDialog<String>(
    context: context,
    builder: (ctx) => AlertDialog(
      title: Text(loc.reauthTitle),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(loc.reauthMessage),
          const SizedBox(height: 16),
          TextField(
            controller: controller,
            obscureText: true,
            autofocus: true,
            decoration: InputDecoration(labelText: loc.passwordLabel),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(ctx, null),
          child: Text(loc.cancelButton),
        ),
        TextButton(
          onPressed: () => Navigator.pop(ctx, controller.text),
          child: Text(loc.confirmButton),
        ),
      ],
    ),
  );
}
