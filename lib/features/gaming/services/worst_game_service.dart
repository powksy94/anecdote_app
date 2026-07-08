import '../data/worst_game_data.dart';
import '../../../core/models/content_data.dart';

class WorstGameService {
  static List<WorstGameData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadWorstGames();
    final g = dailyWorstGame(_cache!);

    final buf = StringBuffer();
    buf.writeln('📅 Year: ${g.year}');
    buf.writeln('🏢 Publisher: ${g.publisher}');
    if (g.score != null) buf.writeln('⭐ Metacritic: ${g.score}/100');
    buf.writeln('💀 ${g.reason}');

    return ContentData(
      preview: '💀 ${g.name} (${g.year})',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: g.imageUrl,
      noImageMessage: g.noImageMessage,
    );
  }
}
