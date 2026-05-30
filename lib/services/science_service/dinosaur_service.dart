import '../../data/dinosaur_data.dart';
import '../../models/content_data.dart';

class DinosaurService {
  static List<DinosaurData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadDinosaurs();
    final d = dailyDinosaur(_cache!);

    final buf = StringBuffer();
    buf.writeln('🕰️ Period: ${d.period}');
    buf.writeln('🍖 Diet: ${d.diet}');
    if (d.length != null) { buf.writeln('📏 Length: ${d.length}m'); }
    if (d.weight != null) {
      final w = d.weight!;
      final fmt = w >= 1000 ? '${(w / 1000).toStringAsFixed(1)}t' : '${w}kg';
      buf.writeln('⚖️ Weight: $fmt');
    }
    if (d.discoveryYear != null) { buf.writeln('📅 Discovered: ${d.discoveryYear}'); }
    buf.writeln('🔭 Described by: ${d.describer}');
    buf.writeln('💡 ${d.famousFor}');

    return ContentData(
      preview: '🦕 ${d.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: d.imageUrl,
      noImageMessage: d.noImageMessage,
    );
  }
}
