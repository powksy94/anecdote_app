import '../data/music_festival_data.dart';
import '../../../core/models/content_data.dart';

class MusicFestivalService {
  static List<MusicFestivalData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadMusicFestivals();
    final f = dailyMusicFestival(_cache!);

    final buf = StringBuffer();
    buf.writeln('📍 Location: ${f.location}');
    buf.writeln('👥 Attendance: ${f.attendance}');
    buf.writeln('🎪 ${f.fact}');

    return ContentData(
      preview: f.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: f.imageUrl,
      noImageMessage: f.noImageMessage,
    );
  }
}
