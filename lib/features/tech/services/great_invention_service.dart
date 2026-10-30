import '../data/great_invention_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class GreatInventionService {
  static List<GreatInventionData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadGreatInventions();
    final e = dailyGreatInvention(_cache!);

    final buf = StringBuffer();
    if (e.inventor != null) {
      buf.writeln('${flagEmoji(e.countryCode)} ${e.inventor}');
    } else if (e.countryCode != null) {
      buf.writeln('${flagEmoji(e.countryCode)} Unknown inventor');
    }
    buf.writeln('🗓️ Year: ${e.year}');
    buf.writeln('💡 ${e.fact}');

    return ContentData(
      preview: e.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: e.imageUrl,
      noImageMessage: e.imageUrl == null ? '📷 No image available for this invention' : null,
    );
  }
}
