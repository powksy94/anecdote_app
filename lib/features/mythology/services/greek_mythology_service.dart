import '../data/greek_mythology_data.dart';
import '../../../core/models/content_data.dart';

class GreekMythologyService {
  static List<GreekMythologyData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadGreekMythology();
    final g = dailyGreekMythology(_cache!);

    final buf = StringBuffer();
    buf.writeln('⚡ Domain: ${g.domain}');
    buf.writeln('🔱 Symbol: ${g.symbol}');
    buf.writeln('📜 ${g.famousFor}');

    return ContentData(
      preview: g.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: g.imageUrl,
      noImageMessage: g.noImageMessage,
    );
  }
}
