import '../data/lgbtqia_data.dart';
import '../../../core/models/content_data.dart';

class LgbtqiaService {
  static List<LgbtqiaData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadLgbtqiaPersonalities();
    final p = dailyLgbtqia(_cache!);

    final buf = StringBuffer();
    if (p.orientation != null) {
      buf.writeln('🏳️‍🌈 Identity: ${p.orientation}');
    }
    buf.writeln('🌍 Country: ${p.country}');
    buf.writeln('🗓️ ${p.years}');
    buf.writeln('🎭 Field: ${p.field}');
    buf.writeln('💡 ${p.impact}');

    return ContentData(
      preview: p.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: p.imageUrl,
      noImageMessage: p.imageUrl == null ? '👤 No portrait available for this personality' : null,
      warningText: p.isOrientationUncertain
          ? 'Sexual orientation or gender identity is uncertain or debated by historians'
          : null,
      warningLevel: p.isOrientationUncertain ? 'orange' : null,
    );
  }
}
