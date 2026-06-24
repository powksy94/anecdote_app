import '../data/sea_data.dart';
import '../../../core/models/content_data.dart';

class SeaService {
  static List<SeaData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSeas();
    final s = dailySea(_cache!);

    final buf = StringBuffer();
    buf.writeln('📍 Location: ${s.location}');
    buf.writeln('🌐 Basin: ${s.ocean}');
    buf.writeln('📏 Area: ${s.area.toString().replaceAllMapped(RegExp(r'\B(?=(\d{3})+(?!\d))'), (m) => ',')} km²');
    buf.writeln('💡 ${s.famousFor}');

    return ContentData(
      preview: '🌊 ${s.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: s.imageUrl,
      noImageMessage: s.noImageMessage,
    );
  }
}
