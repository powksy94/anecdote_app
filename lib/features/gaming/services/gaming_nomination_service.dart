import '../data/gaming_nomination_data.dart';
import '../../../core/models/content_data.dart';

class GamingNominationService {
  static List<GamingNominationData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadGamingNominations();
    final n = dailyGamingNomination(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏆 Award: ${n.awardBody}');
    buf.writeln('📋 Category: ${n.category}');
    buf.writeln('🎮 Game: ${n.name}');
    buf.writeln('🛠️ Developer: ${n.developer}');
    buf.writeln('💡 ${n.description}');

    return ContentData(
      preview: '🏆 ${n.year} — ${n.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: n.imageUrl,
      noImageMessage: n.noImageMessage,
    );
  }
}
