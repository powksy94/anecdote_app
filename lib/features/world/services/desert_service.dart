import '../data/desert_data.dart';
import '../../../core/models/content_data.dart';

class DesertService {
  static List<DesertData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadDeserts();
    final d = dailyDesert(_cache!);

    final buf = StringBuffer();
    buf.writeln('📍 Location: ${d.country}');
    buf.writeln('🏷️ Type: ${d.type}');
    buf.writeln('📏 Area: ${d.area.toString().replaceAllMapped(RegExp(r'\B(?=(\d{3})+(?!\d))'), (m) => ',')} km²');
    buf.writeln('💡 ${d.famousFor}');

    return ContentData(
      preview: '🏜️ ${d.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: d.imageUrl,
      noImageMessage: d.noImageMessage,
    );
  }
}
