import 'package:cloud_firestore/cloud_firestore.dart';
import '../../../core/models/content_type.dart';
import '../models/favorite_fact.dart';

class FavoritesService {
  final String uid;

  FavoritesService(this.uid);

  CollectionReference<Map<String, dynamic>> get _col =>
      FirebaseFirestore.instance
          .collection('users')
          .doc(uid)
          .collection('favorites');

  DocumentReference<Map<String, dynamic>> get _userDoc =>
      FirebaseFirestore.instance.collection('users').doc(uid);

  Stream<List<FavoriteFact>> watchAll() async* {
    await _resetIfMonthChanged();
    yield* _col
        .orderBy('savedAt', descending: true)
        .snapshots()
        .map((snap) => snap.docs
            .map((d) => FavoriteFact.fromFirestore(d))
            .toList());
  }

  Stream<List<FavoriteFact>> watchByCategory(ContentType type) =>
      watchAll().map((list) =>
          list.where((f) => f.contentType == type).toList());

  Future<void> toggle(FavoriteFact fact) async {
    final doc = _col.doc(fact.id);
    if ((await doc.get()).exists) {
      await doc.delete();
    } else {
      await doc.set(fact.toMap());
    }
  }

  Future<bool> isFavorite(String id) async =>
      (await _col.doc(id).get()).exists;

  Future<void> _resetIfMonthChanged() async {
    final now = DateTime.now();
    final current =
        '${now.year}-${now.month.toString().padLeft(2, '0')}';
    final snap = await _userDoc.get();
    final stored = snap.data()?['lastFavoritesMonth'] as String? ?? '';
    if (stored == current) return;

    final batch = FirebaseFirestore.instance.batch();
    final favSnap = await _col.get();
    for (final doc in favSnap.docs) {
      batch.delete(doc.reference);
    }
    batch.update(_userDoc, {'lastFavoritesMonth': current});
    await batch.commit();
  }
}
