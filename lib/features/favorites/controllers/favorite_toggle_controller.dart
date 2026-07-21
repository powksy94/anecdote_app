import 'package:firebase_auth/firebase_auth.dart';
import '../../../core/models/content_type.dart';
import '../models/favorite_fact.dart';
import '../services/favorites_service.dart';

class FavoriteToggleController {
  /// Returns the new [isFavorited] state, or null if the user is not signed in.
  Future<bool?> toggle(ContentType type, String preview,
      {String details = ''}) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return null;

    final fact = FavoriteFact.create(type, preview, details: details);
    final service = FavoritesService(user.uid);
    await service.toggle(fact);
    return service.isFavorite(fact.id);
  }

  Future<bool> isFavorite(ContentType type, String preview) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return false;

    final id = FavoriteFact.buildId(type, preview);
    return FavoritesService(user.uid).isFavorite(id);
  }
}
