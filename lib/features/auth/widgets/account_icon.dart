import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../../subscription/pages/premium_page.dart';
import '../../subscription/services/purchase_service.dart';
import '../pages/login_page.dart';
import '../services/auth_service.dart';
import 'profile_sheet.dart';

class AccountIcon extends StatefulWidget {
  const AccountIcon({super.key});

  @override
  State<AccountIcon> createState() => _AccountIconState();
}

class _AccountIconState extends State<AccountIcon> {
  // Cached once so StreamBuilder never sees a new stream object between rebuilds
  final Stream<bool> _premiumStream = PurchaseService.premiumStream;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return StreamBuilder<User?>(
      stream: AuthService().authStateChanges,
      builder: (context, authSnapshot) {
        final user = authSnapshot.data;
        return StreamBuilder<bool>(
          stream: _premiumStream,
          initialData: false,
          builder: (context, premiumSnapshot) {
            final isPremium = premiumSnapshot.data ?? false;
            return GestureDetector(
              onTap: () => user == null
                  ? _goToLogin(context)
                  : _showProfile(context, user, isPremium),
              child: Stack(
                clipBehavior: Clip.none,
                children: [
                  CircleAvatar(
                    radius: 18,
                    backgroundColor: theme.colorScheme.primaryContainer,
                    child: user != null
                        ? Text(
                            (user.displayName ?? user.email ?? '?')[0]
                                .toUpperCase(),
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: theme.colorScheme.primary,
                            ),
                          )
                        : Icon(Icons.person_outlined,
                            size: 20, color: theme.colorScheme.primary),
                  ),
                  if (isPremium)
                    Positioned(
                      bottom: -1,
                      right: -1,
                      child: Container(
                        width: 14,
                        height: 14,
                        decoration: BoxDecoration(
                          color: const Color(0xFFFFB300),
                          shape: BoxShape.circle,
                          border: Border.all(color: Colors.white, width: 1.5),
                        ),
                        child: const Icon(Icons.star, size: 8, color: Colors.white),
                      ),
                    ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  void _goToLogin(BuildContext context) {
    Navigator.push(
        context, MaterialPageRoute(builder: (_) => const LoginPage()));
  }

  void _showProfile(BuildContext context, User user, bool isPremium) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) => ProfileSheet(
        user: user,
        isPremium: isPremium,
        onPremiumTap: () => Navigator.of(context, rootNavigator: true).push(
          MaterialPageRoute(builder: (_) => const PremiumPage()),
        ),
      ),
    );
  }
}
