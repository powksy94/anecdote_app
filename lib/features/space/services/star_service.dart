import '../data/star_data.dart';
import '../../../core/models/content_data.dart';

class StarService {
  static List<StarData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadStars();
    final s = dailyStar(_cache!);

    final buf = StringBuffer();
    buf.writeln('🔭 Constellation: ${s.constellation}');
    if (s.distance == 0) {
      buf.writeln('📏 Distance: 0 (our Sun)');
    } else {
      buf.writeln('📏 Distance: ${s.distance.toStringAsFixed(2)} ly');
    }
    buf.writeln('✨ Magnitude: ${s.magnitude.toStringAsFixed(2)}');
    buf.writeln('🌡️ Category: ${s.category}');
    if (s.radius != null) {
      buf.writeln('🔵 Radius: ${_formatMultiplier(s.radius!)}× Sun');
    }
    if (s.mass != null) {
      buf.writeln('⚖️ Mass: ${_formatMultiplier(s.mass!)}× Sun');
    }
    buf.writeln('⚡ System: ${s.system}');
    buf.writeln('🌌 Galaxy: ${s.galaxy}');
    if (s.planets > 0) {
      buf.writeln('🪐 Planets: ${s.planets}');
    }

    return ContentData(
      preview: '⭐ ${s.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: s.imageUrl,
      noImageMessage: s.noImageMessage,
    );
  }

  String _formatMultiplier(double value) {
    if (value >= 1000) return value.toStringAsFixed(0);
    if (value >= 10)   return value.toStringAsFixed(1);
    if (value >= 1)    return value.toStringAsFixed(2);
    return value.toStringAsFixed(4);
  }
}
