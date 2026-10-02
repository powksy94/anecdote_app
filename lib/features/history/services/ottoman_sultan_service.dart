import '../data/ottoman_sultan_data.dart';
import '../../../core/models/content_data.dart';

class OttomanSultanService {
  static List<OttomanSultanData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadOttomanSultans();
    final s = dailyOttomanSultan(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏛️ Era: ${s.era}');
    if (s.nickname != null) { buf.writeln('🏷️ Nickname: ${s.nickname}'); }
    buf.writeln('📅 Reign: ${s.reignStart} to ${s.reignEnd}');
    buf.writeln('⚜️ Famous for: ${s.famousFor}');

    return ContentData(
      preview: '🇹🇷 ${s.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: s.imageUrl,
      noImageMessage: s.noImageMessage,
      imageNote: s.historicalNote,
    );
  }
}
