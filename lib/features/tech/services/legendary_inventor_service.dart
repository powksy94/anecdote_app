import '../data/legendary_inventor_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class LegendaryInventorService {
  static List<LegendaryInventorData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadLegendaryInventors();
    final i = dailyLegendaryInventor(_cache!);

    final buf = StringBuffer();
    buf.writeln('🛠️ Invention: ${i.invention}');
    buf.writeln('${flagEmoji(i.countryCode)} ${i.years ?? ''}'.trim());
    buf.writeln('💡 ${i.fact}');

    return ContentData(
      preview: i.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: i.imageUrl,
      noImageMessage: i.imageUrl == null ? '👤 No portrait available for this inventor' : null,
      lifeDatesUndocumented: i.years == null,
    );
  }
}
