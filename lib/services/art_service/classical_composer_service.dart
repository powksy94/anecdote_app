import '../../data/classical_composer_data.dart';
import '../../models/content_data.dart';

class ClassicalComposerService {
  static List<ClassicalComposerData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadClassicalComposers();
    final c = dailyClassicalComposer(_cache!);

    final buf = StringBuffer();
    buf.writeln('🌍 Nationality: ${c.nationality}');
    final lifespan = c.died == '-' ? 'b. ${c.born}' : '${c.born} – ${c.died}';
    buf.writeln('🗓️ $lifespan');
    buf.writeln('🎵 Period: ${c.period}');
    buf.writeln('🎼 Famous works: ${c.famousWorks}');
    buf.writeln('💡 ${c.famousFor}');

    return ContentData(
      preview: c.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: c.imageUrl,
      noImageMessage: c.noImageMessage,
    );
  }
}
