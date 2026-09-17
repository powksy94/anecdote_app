import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../controllers/account_deletion_controller.dart';
import 'delete_account_confirm_dialog.dart';
import 'reauth_password_dialog.dart';

class DeleteAccountTile extends StatefulWidget {
  const DeleteAccountTile({super.key});

  @override
  State<DeleteAccountTile> createState() => _DeleteAccountTileState();
}

class _DeleteAccountTileState extends State<DeleteAccountTile> {
  final _controller = AccountDeletionController();
  bool _isDeleting = false;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return ListTile(
      leading: _isDeleting
          ? const SizedBox(
              width: 24, height: 24,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Icon(Icons.delete_forever_rounded, color: theme.colorScheme.error),
      title: Text(
        loc.deleteAccount,
        style: TextStyle(color: theme.colorScheme.error),
      ),
      onTap: _isDeleting ? null : _handleTap,
    );
  }

  Future<void> _handleTap() async {
    final confirmed = await showDeleteAccountConfirmDialog(context);
    if (!confirmed || !context.mounted) return;

    // Le mot de passe est toujours redemandé ici, avant toute suppression :
    // ça garantit une session fraîche pour toute l'opération et évite de
    // supprimer les données Firestore puis d'échouer sur la suppression du
    // compte Auth (requires-recent-login), ce qui laisserait le compte actif
    // sans ses données.
    final password = await showReauthPasswordDialog(context);
    if (password == null || !context.mounted) return;

    setState(() => _isDeleting = true);
    final errorCode = await _controller.reauthenticateAndDelete(password);

    if (!context.mounted) return;
    if (errorCode == null) {
      Navigator.pop(context);
    } else {
      setState(() => _isDeleting = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(AppLocalizations.of(context)!.deleteAccountError)),
      );
    }
  }
}
