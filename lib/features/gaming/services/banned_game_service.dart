import '../data/banned_game_data.dart';
import '../../../core/models/content_data.dart';

class BannedGameService {
  static List<BannedGameData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadBannedGames();
    final g = dailyBannedGame(_cache!);

    final buf = StringBuffer();
    buf.writeln('📅 Year: ${g.year}');
    buf.writeln('🛠️ Developer: ${g.developer}');
    buf.writeln('🚫 Banned in: ${g.bannedIn}');
    buf.writeln('💡 ${g.reason}');

    return ContentData(
      preview: '🚫 ${g.name} (${g.year})',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: g.imageUrl,
      noImageMessage: g.noImageMessage,
      protectedTerms: [g.name],
    );
  }
}
