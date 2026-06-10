import '../data/photographer_data.dart';
import '../../../core/models/content_data.dart';

class PhotographerService {
  static List<PhotographerData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadPhotographers();
    final p = dailyPhotographer(_cache!);

    final buf = StringBuffer();
    buf.writeln('🌍 Nationality: ${p.nationality}');
    final lifespan = p.died == '-' ? 'b. ${p.born}' : '${p.born} – ${p.died}';
    buf.writeln('🗓️ $lifespan');
    buf.writeln('📷 Style: ${p.style}');
    buf.writeln('🖼️ Famous work: ${p.famousWork}');
    buf.writeln('💡 ${p.famousFor}');

    return ContentData(
      preview: p.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: p.imageUrl,
      noImageMessage: p.noImageMessage,
      warningText: p.warningText,
      warningLevel: p.warningLevel,
    );
  }
}
