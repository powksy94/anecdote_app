import '../data/sport_great_woman_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class SportGreatWomanService {
  static List<SportGreatWomanData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSportGreatWomen();
    final w = dailySportGreatWoman(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏅 Sport: ${w.sport}');
    buf.writeln('${flagEmoji(w.countryCode)} ${w.years}');
    buf.writeln('🏛️ Era context: ${w.context}');
    buf.writeln('💡 ${w.achievement}');

    return ContentData(
      preview: w.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: w.imageUrl,
      noImageMessage: w.imageUrl == null ? '👤 No portrait available for this athlete' : null,
    );
  }
}
