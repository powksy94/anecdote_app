import '../data/music_legend_data.dart';
import '../../../core/models/content_data.dart';

class MusicLegendService {
  static List<MusicLegendData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadMusicLegends();
    final l = dailyMusicLegend(_cache!);

    final buf = StringBuffer();
    buf.writeln('🎵 Genre: ${l.genre}');
    buf.writeln('⭐ Famous for: ${l.famousFor}');

    return ContentData(
      preview: l.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: l.imageUrl,
      noImageMessage: l.noImageMessage,
      warningText: l.warningText,
      warningLevel: l.warningLevel,
    );
  }
}
