import '../data/pioneer_woman_data.dart';
import '../../../core/models/content_data.dart';

class PioneerWomanService {
  static List<PioneerWomanData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadPioneerWomen();
    final w = dailyPioneerWoman(_cache!);

    final buf = StringBuffer();
    buf.writeln('🌍 Country: ${w.country}');
    buf.writeln('🗓️ ${w.years}');
    buf.writeln('🔬 Field: ${w.field}');
    buf.writeln('🏛️ Era context: ${w.context}');
    buf.writeln('💡 ${w.impact}');

    return ContentData(
      preview: w.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: w.imageUrl,
      noImageMessage: w.imageUrl == null ? '👤 No portrait available for this pioneer' : null,
    );
  }
}
