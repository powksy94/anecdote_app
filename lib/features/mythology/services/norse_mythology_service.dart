import '../data/norse_mythology_data.dart';
import '../../../core/models/content_data.dart';

class NorseMythologyService {
  static List<NorseMythologyData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadNorseMythology();
    final n = dailyNorseMythology(_cache!);

    final buf = StringBuffer();
    buf.writeln('⚡ Domain: ${n.domain}');
    buf.writeln('🔱 Symbol: ${n.symbol}');
    buf.writeln('📜 ${n.famousFor}');

    return ContentData(
      preview: n.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: n.imageUrl,
      noImageMessage: n.noImageMessage,
    );
  }
}
