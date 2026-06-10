import '../data/sculpture_data.dart';
import '../../../core/models/content_data.dart';

class SculptureService {
  static List<SculptureData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSculptures();
    final s = dailySculpture(_cache!);

    final buf = StringBuffer();
    buf.writeln('🎨 Artist: ${s.artist}');
    buf.writeln('📅 Year: ${s.year}');
    buf.writeln('🪨 Material: ${s.material}');
    buf.writeln('🎭 Style: ${s.style}');
    buf.writeln('📍 Location: ${s.location}');
    buf.writeln('💡 ${s.famousFor}');

    return ContentData(
      preview: s.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: s.imageUrl,
      noImageMessage: s.noImageMessage,
    );
  }
}
