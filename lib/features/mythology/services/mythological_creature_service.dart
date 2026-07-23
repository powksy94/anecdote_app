import '../data/mythological_creature_data.dart';
import '../../../core/models/content_data.dart';

class MythologicalCreatureService {
  static List<MythologicalCreatureData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadMythologicalCreatures();
    final c = dailyMythologicalCreature(_cache!);

    final buf = StringBuffer();
    buf.writeln('🌍 Origin: ${c.origin}');
    buf.writeln('📜 ${c.fact}');
    buf.writeln('⚔️ Fate: ${c.defeatedBy}');

    return ContentData(
      preview: c.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: c.imageUrl,
      noImageMessage: c.noImageMessage,
    );
  }
}
