import '../data/chinese_dynasty_data.dart';
import '../../../core/models/content_data.dart';

class ChineseDynastyService {
  static List<ChineseDynastyData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadChineseDynasties();
    final d = dailyChineseDynasty(_cache!);

    final buf = StringBuffer();
    final start = ChineseDynastyData.formatYear(d.reignStart);
    final end = ChineseDynastyData.formatYear(d.reignEnd);
    buf.writeln('📅 Period: $start to $end');
    buf.writeln('🏮 Famous for: ${d.famousFor}');

    return ContentData(
      preview: '🇨🇳 ${d.name} dynasty',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: d.imageUrl,
      noImageMessage: d.noImageMessage,
      imageNote: d.historicalNote,
    );
  }
}
