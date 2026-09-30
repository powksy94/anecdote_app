import '../data/diplomatic_scandal_data.dart';
import '../../../core/models/content_data.dart';
import '../../../core/utils/flag_emoji.dart';

class DiplomaticScandalService {
  static List<DiplomaticScandalData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadDiplomaticScandals();
    final s = dailyDiplomaticScandal(_cache!);

    final buf = StringBuffer();
    buf.writeln('${flagEmoji(s.countryCode)} ${s.year}');
    buf.writeln('🌍 Context: ${s.context}');
    buf.writeln('💡 ${s.fact}');

    return ContentData(
      preview: s.title,
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}
