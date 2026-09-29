import '../data/sport_record_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class SportRecordService {
  static List<SportRecordData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSportRecords();
    final r = dailySportRecord(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏅 Sport: ${r.sport}');
    if (r.holder != null) {
      buf.writeln('${flagEmoji(r.countryCode)} Holder: ${r.holder}');
    }
    buf.writeln('🗓️ Year: ${r.year}');
    buf.writeln('💡 ${r.fact}');

    return ContentData(
      preview: r.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: r.imageUrl,
      noImageMessage: r.imageUrl == null ? '📷 No photo available for this record' : null,
    );
  }
}
