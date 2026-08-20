import '../data/independent_musician_data.dart';
import '../../../core/models/content_data.dart';

class IndependentMusicianService {
  static List<IndependentMusicianData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadIndependentMusicians();
    final a = dailyIndependentMusician(_cache!);

    final buf = StringBuffer();
    buf.writeln('🎵 Genre: ${a.genre}');
    buf.writeln('🎧 Signature song: ${a.famousSong}');
    buf.writeln('⭐ Known for: ${a.famousFor}');

    return ContentData(
      preview: a.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: a.imageUrl,
      noImageMessage: a.noImageMessage,
    );
  }
}
