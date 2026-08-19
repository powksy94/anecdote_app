import '../data/mountain_data.dart';
import '../../../core/models/content_data.dart';

class MountainService {
  static List<MountainData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadMountains();
    final m = dailyMountain(_cache!);

    final buf = StringBuffer();
    buf.writeln('📍 Location: ${m.country}');
    buf.writeln('⛰️ Range: ${m.range}');
    buf.writeln('📏 Elevation: ${m.elevation} m');
    if (m.firstAscent != null) {
      buf.writeln('🧗 First ascent: ${m.firstAscent}');
    }
    buf.writeln('💡 ${m.famousFor}');

    return ContentData(
      preview: '🏔️ ${m.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: m.imageUrl,
      noImageMessage: m.noImageMessage,
    );
  }
}
