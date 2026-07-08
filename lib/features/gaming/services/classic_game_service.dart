import '../data/classic_game_data.dart';
import '../../../core/models/content_data.dart';

class ClassicGameService {
  static List<ClassicGameData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadClassicGames();
    final g = dailyClassicGame(_cache!);

    final buf = StringBuffer();
    buf.writeln('📅 Year: ${g.year}');
    buf.writeln('🛠️ Developer: ${g.developer}');
    buf.writeln('🎯 Genre: ${g.genre}');
    buf.writeln('💡 ${g.famousFor}');

    return ContentData(
      preview: '🕹️ ${g.name} (${g.year})',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: g.imageUrl,
      noImageMessage: g.noImageMessage,
    );
  }
}
