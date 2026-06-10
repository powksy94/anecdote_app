import '../data/nobel_prize_data.dart';
import '../../../core/models/content_data.dart';

class NobelPrizeService {
  static List<NobelPrizeData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadNobelPrizes();
    final n = dailyNobelPrize(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏆 Prize year: ${n.year}');
    buf.writeln('📚 Category: ${n.category}');
    buf.writeln('🌍 Country: ${n.country}');
    buf.writeln('💡 ${n.famousFor}');

    return ContentData(
      preview: n.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: n.imageUrl,
      noImageMessage: n.noImageMessage,
      warningText: n.warningText,
      warningLevel: n.warningLevel,
    );
  }
}
