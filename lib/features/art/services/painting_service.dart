import '../data/painting_data.dart';
import '../../../core/models/content_data.dart';

class PaintingService {
  static List<PaintingData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadPaintings();
    final p = dailyPainting(_cache!);

    final buf = StringBuffer();
    buf.writeln('🎨 Artist: ${p.artist}');
    buf.writeln('📅 Year: ${p.year}');
    buf.writeln('🖌️ Medium: ${p.medium}');
    buf.writeln('🏛️ Style: ${p.style}');
    buf.writeln('📍 Location: ${p.museum}');
    buf.writeln('💡 ${p.famousFor}');

    return ContentData(
      preview: '🖼️ ${p.title}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: p.imageUrl,
      noImageMessage: p.noImageMessage,
    );
  }
}
