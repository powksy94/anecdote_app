import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../services/auth_service.dart';
import 'login_page.dart';
import 'register_page.dart';

class WelcomePage extends StatelessWidget {
  final VoidCallback onProceed;

  const WelcomePage({super.key, required this.onProceed});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return StreamBuilder<User?>(
      stream: AuthService().authStateChanges,
      builder: (context, snapshot) {
        if (snapshot.data != null) {
          WidgetsBinding.instance.addPostFrameCallback((_) => onProceed());
        }
        return Scaffold(
          body: SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 32),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Spacer(),
                  Icon(Icons.lightbulb_rounded,
                      size: 72, color: theme.colorScheme.primary),
                  const SizedBox(height: 24),
                  Text(
                    loc.welcomeTitle,
                    style: theme.textTheme.headlineMedium
                        ?.copyWith(fontWeight: FontWeight.bold),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    loc.welcomeSubtitle,
                    style: theme.textTheme.bodyLarge?.copyWith(
                      color: theme.colorScheme.onSurface.withValues(alpha: 0.65),
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const Spacer(),
                  FilledButton(
                    onPressed: () => Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const RegisterPage()),
                    ),
                    child: Text(loc.createAccount),
                  ),
                  const SizedBox(height: 12),
                  OutlinedButton(
                    onPressed: () => Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const LoginPage()),
                    ),
                    child: Text(loc.signIn),
                  ),
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: onProceed,
                    child: Text(loc.continueWithoutAccount),
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
