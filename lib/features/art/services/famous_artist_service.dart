import '../data/famous_artist_data.dart';
import '../../../core/models/content_data.dart';

class FamousArtistService {
  static List<FamousArtistData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadFamousArtists();
    final a = dailyFamousArtist(_cache!);

    final buf = StringBuffer();
    buf.writeln('🌍 Nationality: ${a.nationality}');
    final lifespan = a.died == '-' ? 'b. ${a.born}' : '${a.born} – ${a.died}';
    buf.writeln('🗓️ $lifespan');
    buf.writeln('🎭 Movement: ${a.movement}');
    buf.writeln('💡 ${a.famousFor}');

    return ContentData(
      preview: a.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: a.imageUrl,
      noImageMessage: a.noImageMessage,
      warningText: a.warningText,
      warningLevel: a.warningLevel,
    );
  }
}
