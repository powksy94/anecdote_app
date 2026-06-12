import '../data/mineral_data.dart';
import '../../../core/models/content_data.dart';

class MineralService {
  static List<MineralData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadMinerals();
    final m = dailyMineral(_cache!);

    final buf = StringBuffer();
    buf.writeln('🔬 Group: ${m.group}  |  Crystal system: ${m.crystalSystem}');
    buf.writeln('⚒️ Hardness: ${m.hardness} (Mohs scale)  |  Discovered: ${m.discovery}');
    buf.writeln('🎨 Color: ${m.color}  |  Luster: ${m.luster}');
    buf.writeln('⚙️ Annual production: ${m.production}');
    buf.writeln('🏭 Uses: ${m.uses}');
    buf.writeln('💡 ${m.famousFor}');

    return ContentData(
      preview: '💎 ${m.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: m.imageUrl,
      noImageMessage: m.noImageMessage,
    );
  }
}
