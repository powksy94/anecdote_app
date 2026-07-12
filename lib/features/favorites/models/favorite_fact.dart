import 'package:cloud_firestore/cloud_firestore.dart';
import '../../../core/models/content_type.dart';

class FavoriteFact {
  final String id;
  final ContentType contentType;
  final String preview;
  final DateTime savedAt;
  final String month;

  const FavoriteFact({
    required this.id,
    required this.contentType,
    required this.preview,
    required this.savedAt,
    required this.month,
  });

  static String buildId(ContentType type, String preview) =>
      '${type.name}_${preview.hashCode.abs()}';

  static String _currentMonth() {
    final now = DateTime.now();
    return '${now.year}-${now.month.toString().padLeft(2, '0')}';
  }

  factory FavoriteFact.create(ContentType type, String preview) {
    final now = DateTime.now();
    return FavoriteFact(
      id: buildId(type, preview),
      contentType: type,
      preview: preview,
      savedAt: now,
      month: _currentMonth(),
    );
  }

  factory FavoriteFact.fromFirestore(
      DocumentSnapshot<Map<String, dynamic>> doc) {
    final d = doc.data()!;
    return FavoriteFact(
      id: doc.id,
      contentType: ContentType.values
          .firstWhere((e) => e.name == d['contentType'] as String),
      preview: d['preview'] as String,
      savedAt: DateTime.parse(d['savedAt'] as String),
      month: d['month'] as String,
    );
  }

  Map<String, dynamic> toMap() => {
        'contentType': contentType.name,
        'preview': preview,
        'savedAt': savedAt.toIso8601String(),
        'month': month,
      };
}
