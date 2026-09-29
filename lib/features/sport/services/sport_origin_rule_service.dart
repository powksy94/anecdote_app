import '../data/sport_origin_rule_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class SportOriginRuleService {
  static List<SportOriginRuleData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSportOriginRules();
    final r = dailySportOriginRule(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏅 Sport: ${r.sport}');
    buf.writeln('${flagEmoji(r.countryCode)} ${r.year}');
    buf.writeln('💡 ${r.fact}');

    return ContentData(
      preview: r.title,
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}
