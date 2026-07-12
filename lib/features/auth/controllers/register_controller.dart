import 'package:firebase_auth/firebase_auth.dart';
import '../services/auth_service.dart';

class RegisterController {
  /// Returns null on success, or the Firebase error code on failure.
  Future<String?> createAccount({
    required String email,
    required String password,
    required String displayName,
    required Set<String> categories,
  }) async {
    try {
      await AuthService().registerWithEmail(
        email: email,
        password: password,
        displayName: displayName,
        favoriteCategories: categories.toList(),
      );
      return null;
    } on FirebaseAuthException catch (e) {
      return e.code;
    }
  }
}
