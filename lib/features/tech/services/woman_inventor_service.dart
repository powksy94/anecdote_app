import '../data/woman_inventor_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class WomanInventorService {
  static List<WomanInventorData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadWomanInventors();
    final w = dailyWomanInventor(_cache!);

    final buf = StringBuffer();
    buf.writeln('🛠️ Invention: ${w.invention}');
    buf.writeln('${flagEmoji(w.countryCode)} ${w.years ?? ''}'.trim());
    if (w.context != null) buf.writeln('🏛️ Era context: ${w.context}');
    buf.writeln('💡 ${w.fact}');

    return ContentData(
      preview: w.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: w.imageUrl,
      noImageMessage: w.imageUrl == null ? '👤 No portrait available for this inventor' : null,
      lifeDatesUndocumented: w.years == null,
    );
  }
}
