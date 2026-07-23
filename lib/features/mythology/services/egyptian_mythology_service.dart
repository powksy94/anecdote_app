import '../data/egyptian_mythology_data.dart';
import '../../../core/models/content_data.dart';

class EgyptianMythologyService {
  static List<EgyptianMythologyData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadEgyptianMythology();
    final e = dailyEgyptianMythology(_cache!);

    final buf = StringBuffer();
    buf.writeln('⚡ Domain: ${e.domain}');
    buf.writeln('🔱 Symbol: ${e.symbol}');
    buf.writeln('📜 ${e.famousFor}');

    return ContentData(
      preview: e.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: e.imageUrl,
      noImageMessage: e.noImageMessage,
    );
  }
}
