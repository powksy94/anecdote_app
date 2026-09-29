import '../data/sport_legendary_event_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class SportLegendaryEventService {
  static List<SportLegendaryEventData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSportLegendaryEvents();
    final e = dailySportLegendaryEvent(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏅 Sport: ${e.sport}');
    if (e.protagonist != null) {
      buf.writeln('${flagEmoji(e.countryCode)} ${e.protagonist}');
    }
    buf.writeln('🗓️ Year: ${e.year}');
    buf.writeln('💡 ${e.fact}');

    return ContentData(
      preview: e.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: e.imageUrl,
      noImageMessage: e.imageUrl == null ? '📷 No photo available for this moment' : null,
    );
  }
}
