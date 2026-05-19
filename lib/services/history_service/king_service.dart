import '../../data/king_of_france_data.dart';
import '../../models/content_data.dart';

class KingService {
  static List<KingOfFranceData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadKingsOfFrance();
    final k = dailyKingOfFrance(_cache!);

    final buf = StringBuffer();
    buf.writeln('👑 Dynasty: ${k.dynasty}');
    if (k.nickname != null) { buf.writeln('🏷️ Nickname: ${k.nickname}'); }
    final reignEnd = k.reignEnd == 0 ? 'present' : '${k.reignEnd}';
    buf.writeln('📅 Reign: ${k.reignStart} – $reignEnd');
    buf.writeln('⚜️ Famous for: ${k.famousFor}');

    return ContentData(
      preview: '🇫🇷 ${k.name}',
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}
