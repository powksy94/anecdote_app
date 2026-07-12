import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../pages/login_page.dart';
import '../services/auth_service.dart';

class AccountIcon extends StatelessWidget {
  const AccountIcon({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return StreamBuilder<User?>(
      stream: AuthService().authStateChanges,
      builder: (context, snapshot) {
        final user = snapshot.data;
        return GestureDetector(
          onTap: () => user == null
              ? _goToLogin(context)
              : _showProfile(context, user),
          child: CircleAvatar(
            radius: 18,
            backgroundColor: theme.colorScheme.primaryContainer,
            child: user != null
                ? Text(
                    (user.displayName ?? user.email ?? '?')[0].toUpperCase(),
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: theme.colorScheme.primary,
                    ),
                  )
                : Icon(Icons.person_outlined, size: 20, color: theme.colorScheme.primary),
          ),
        );
      },
    );
  }

  void _goToLogin(BuildContext context) {
    Navigator.push(context, MaterialPageRoute(builder: (_) => const LoginPage()));
  }

  void _showProfile(BuildContext context, User user) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) => _ProfileSheet(user: user),
    );
  }
}

class _ProfileSheet extends StatelessWidget {
  final User user;
  const _ProfileSheet({required this.user});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 16, 24, 32),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 40, height: 4,
            decoration: BoxDecoration(
              color: theme.colorScheme.outlineVariant,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(height: 20),
          CircleAvatar(
            radius: 32,
            backgroundColor: theme.colorScheme.primaryContainer,
            child: Text(
              (user.displayName ?? user.email ?? '?')[0].toUpperCase(),
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: theme.colorScheme.primary,
              ),
            ),
          ),
          const SizedBox(height: 12),
          if (user.displayName != null)
            Text(user.displayName!,
                style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
          Text(user.email ?? '',
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.outline)),
          const SizedBox(height: 24),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.logout_rounded),
            title: Text(loc.signOut),
            onTap: () async {
              Navigator.pop(context);
              await AuthService().signOut();
            },
          ),
        ],
      ),
    );
  }
}
