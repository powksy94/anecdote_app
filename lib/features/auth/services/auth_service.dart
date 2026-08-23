import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  final _auth = FirebaseAuth.instance;
  final _db = FirebaseFirestore.instance;

  Stream<User?> get authStateChanges => _auth.authStateChanges();
  User? get currentUser => _auth.currentUser;

  Future<void> signInWithEmail(String email, String password) async {
    await _auth.signInWithEmailAndPassword(email: email, password: password);
  }

  Future<void> registerWithEmail({
    required String email,
    required String password,
    required String displayName,
    required List<String> favoriteCategories,
  }) async {
    final credential = await _auth.createUserWithEmailAndPassword(
      email: email,
      password: password,
    );
    await credential.user?.updateDisplayName(displayName);
    await _db.collection('users').doc(credential.user!.uid).set({
      'displayName': displayName,
      'email': email,
      'favoriteCategories': favoriteCategories,
      'createdAt': FieldValue.serverTimestamp(),
      'lastFavoritesMonth': '',
    });
  }

  Future<void> signOut() => _auth.signOut();

  /// Deletes the signed-in user's Firestore data and Firebase Auth account.
  /// Throws [FirebaseAuthException] with code 'requires-recent-login' if the
  /// session is too old — call [reauthenticate] then retry in that case.
  Future<void> deleteAccount() async {
    final user = _auth.currentUser;
    if (user == null) return;

    final favorites = await _db
        .collection('users').doc(user.uid).collection('favorites').get();
    final batch = _db.batch();
    for (final doc in favorites.docs) {
      batch.delete(doc.reference);
    }
    batch.delete(_db.collection('users').doc(user.uid));
    await batch.commit();

    await user.delete();
  }

  Future<void> reauthenticate(String password) async {
    final user = _auth.currentUser;
    if (user == null || user.email == null) return;
    final credential =
        EmailAuthProvider.credential(email: user.email!, password: password);
    await user.reauthenticateWithCredential(credential);
  }
}
