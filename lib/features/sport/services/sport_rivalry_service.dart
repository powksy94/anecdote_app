import '../data/sport_rivalry_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class SportRivalryService {
  static List<SportRivalryData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSportRivalries();
    final r = dailySportRivalry(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏅 Sport: ${r.sport}');
    buf.writeln('${flagEmoji(r.countryCode)} ${r.years}');
    buf.writeln('⚔️ Context: ${r.context}');
    buf.writeln('💡 ${r.fact}');

    return ContentData(
      preview: r.name,
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}
