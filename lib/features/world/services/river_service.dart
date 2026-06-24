import '../data/river_data.dart';
import '../../../core/models/content_data.dart';

class RiverService {
  static List<RiverData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadRivers();
    final r = dailyRiver(_cache!);

    final buf = StringBuffer();
    buf.writeln('📍 Countries: ${r.country}');
    buf.writeln('📏 Length: ${r.length} km');
    buf.writeln('🌊 Empties into: ${r.mouth}');
    buf.writeln('💡 ${r.famousFor}');

    return ContentData(
      preview: '🏞️ ${r.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: r.imageUrl,
      noImageMessage: r.noImageMessage,
    );
  }
}
