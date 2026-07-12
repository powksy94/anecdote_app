import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../../auth/services/auth_service.dart';
import '../widgets/favorites_login_prompt.dart';
import 'favorites_page.dart';

class FavoritesGate extends StatelessWidget {
  const FavoritesGate({super.key});

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: AuthService().authStateChanges,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }
        if (snapshot.data == null) {
          return const FavoritesLoginPrompt();
        }
        return const FavoritesPage();
      },
    );
  }
}
