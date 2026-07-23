import '../data/album_data.dart';
import '../../../core/models/content_data.dart';

class AlbumService {
  static List<AlbumData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadAlbums();
    final a = dailyAlbum(_cache!);

    final buf = StringBuffer();
    buf.writeln('🎤 Artist: ${a.artist}');
    buf.writeln('📅 Year: ${a.year}');
    buf.writeln('💰 Sales: ${a.sales}');
    buf.writeln('⭐ ${a.famousFor}');

    return ContentData(
      preview: a.title,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: a.imageUrl,
      noImageMessage: a.noImageMessage,
    );
  }
}
