import '../../data/battle_data.dart';
import '../../models/content_data.dart';

class BattleService {
  static List<BattleData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadBattles();
    final b = dailyBattle(_cache!);

    final buf = StringBuffer();
    buf.writeln('📅 Date: ${b.date}');
    buf.writeln('📍 Location: ${b.location}');
    buf.writeln('⚔️ Belligerents: ${b.belligerents}');
    buf.writeln('🏆 Result: ${b.result}');
    buf.writeln('💡 ${b.famousFor}');

    return ContentData(
      preview: '⚔️ ${b.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: b.imageUrl,
      noImageMessage: b.noImageMessage,
    );
  }
}
