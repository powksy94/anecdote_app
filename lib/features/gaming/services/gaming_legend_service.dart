import '../data/gaming_legend_data.dart';
import '../../../core/models/content_data.dart';

class GamingLegendService {
  static List<GamingLegendData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadGamingLegends();
    final l = dailyGamingLegend(_cache!);

    final buf = StringBuffer();
    buf.writeln('🌍 Nationality: ${l.nationality}');
    buf.writeln('🎮 Specialty: ${l.specialty}');
    buf.writeln('🏆 ${l.achievements}');

    return ContentData(
      preview: '⭐ ${l.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: l.imageUrl,
      noImageMessage: l.noImageMessage,
    );
  }
}
