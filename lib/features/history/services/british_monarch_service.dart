import '../data/british_monarch_data.dart';
import '../../../core/models/content_data.dart';

class BritishMonarchService {
  static List<BritishMonarchData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadBritishMonarchs();
    final m = dailyBritishMonarch(_cache!);

    final buf = StringBuffer();
    buf.writeln('👑 House: ${m.dynasty}');
    if (m.nickname != null) { buf.writeln('🏷️ Nickname: ${m.nickname}'); }
    final reignEnd = m.reignEnd?.toString() ?? 'present';
    buf.writeln('📅 Reign: ${m.reignStart} to $reignEnd');
    buf.writeln('⚜️ Famous for: ${m.famousFor}');

    return ContentData(
      preview: '🇬🇧 ${m.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: m.imageUrl,
      noImageMessage: m.noImageMessage,
      imageNote: m.historicalNote,
    );
  }
}
