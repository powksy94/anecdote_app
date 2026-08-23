import 'package:firebase_auth/firebase_auth.dart';
import '../services/auth_service.dart';

class AccountDeletionController {
  /// Returns null on success, or the Firebase error code on failure
  /// (e.g. 'requires-recent-login' if the session is too old).
  Future<String?> delete() async {
    try {
      await AuthService().deleteAccount();
      return null;
    } on FirebaseAuthException catch (e) {
      return e.code;
    } catch (_) {
      return 'unknown';
    }
  }

  /// Re-authenticates with [password] then retries deletion.
  /// Returns null on success, or an error code on failure.
  Future<String?> reauthenticateAndDelete(String password) async {
    try {
      await AuthService().reauthenticate(password);
    } on FirebaseAuthException catch (e) {
      return e.code;
    } catch (_) {
      return 'unknown';
    }
    return delete();
  }
}
