import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../services/auth_service.dart';

class ProfileSheet extends StatelessWidget {
  final User user;
  final bool isPremium;
  final VoidCallback onPremiumTap;

  const ProfileSheet({
    super.key,
    required this.user,
    required this.isPremium,
    required this.onPremiumTap,
  });

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
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: theme.colorScheme.outlineVariant,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(height: 20),
          Stack(
            children: [
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
              if (isPremium)
                Positioned(
                  bottom: 0,
                  right: 0,
                  child: Container(
                    width: 20,
                    height: 20,
                    decoration: BoxDecoration(
                      color: const Color(0xFFFFB300),
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white, width: 2),
                    ),
                    child: const Icon(Icons.star, size: 12, color: Colors.white),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 12),
          if (user.displayName != null)
            Text(
              user.displayName!,
              style: theme.textTheme.titleMedium
                  ?.copyWith(fontWeight: FontWeight.bold),
            ),
          Text(
            user.email ?? '',
            style: theme.textTheme.bodySmall
                ?.copyWith(color: theme.colorScheme.outline),
          ),
          const SizedBox(height: 24),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.star_rounded, color: Color(0xFFFFB300)),
            title: Text(loc.premiumTitle),
            subtitle: isPremium ? Text(loc.premiumActive) : null,
            trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 16),
            onTap: () {
              Navigator.pop(context);
              onPremiumTap();
            },
          ),
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
