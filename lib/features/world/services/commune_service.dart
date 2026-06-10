import '../data/commune_data.dart';
import '../../../core/models/content_data.dart';

class CommuneService {
  static List<CommuneData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadCommunes();
    final c = dailyCommune(_cache!);

    final buf = StringBuffer();
    buf.writeln('📍 Département: ${c.department}');
    buf.writeln('🌐 Région: ${c.region}');
    if (c.population != null) {
      buf.writeln('👥 Population: ${_formatPop(c.population!)}');
    }
    if (c.area != null) {
      buf.writeln('📐 Superficie: ${c.area} km²');
    }
    buf.writeln('💡 ${c.famousFor}');

    return ContentData(
      preview: '🏘️ ${c.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: c.imageUrl,
      noImageMessage: c.noImageMessage,
    );
  }

  String _formatPop(int pop) {
    if (pop >= 1000000000) return '${(pop / 1e9).toStringAsFixed(1)}B';
    if (pop >= 1000000)    return '${(pop / 1e6).toStringAsFixed(1)}M';
    if (pop >= 1000)       return '${(pop / 1000).toStringAsFixed(0)}K';
    return '$pop';
  }
}
