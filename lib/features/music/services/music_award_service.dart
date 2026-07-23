import '../data/music_award_data.dart';
import '../../../core/models/content_data.dart';

class MusicAwardService {
  static List<MusicAwardData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadMusicAwards();
    final a = dailyMusicAward(_cache!);

    final buf = StringBuffer();
    buf.writeln('🎤 Artist: ${a.artist}');
    buf.writeln('🏆 Award: ${a.award}');
    buf.writeln('📅 Year: ${a.year}');
    buf.writeln('⭐ ${a.fact}');

    return ContentData(
      preview: a.title,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: a.imageUrl,
      noImageMessage: a.noImageMessage,
    );
  }
}
