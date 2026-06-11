import '../data/volcano_data.dart';
import '../../../core/models/content_data.dart';

class VolcanoService {
  static List<VolcanoData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadVolcanoes();
    final v = dailyVolcano(_cache!);

    final buf = StringBuffer();
    buf.writeln('📍 Location: ${v.location}, ${v.country}');
    buf.writeln('🏔️ Type: ${v.type}');
    buf.writeln('🔴 Status: ${v.status}');
    if (v.elevation != null) {
      final elev = v.elevation!;
      final fmt = elev < 0 ? '${elev.abs()} m below sea level' : '$elev m';
      buf.writeln('📏 Elevation: $fmt');
    }
    buf.writeln('🕰️ Last eruption: ${v.lastEruption}');
    buf.writeln('💡 ${v.famousFor}');

    return ContentData(
      preview: '🌋 ${v.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: v.imageUrl,
      noImageMessage: v.noImageMessage,
    );
  }
}
