import '../data/human_bone_data.dart';
import '../../../core/models/content_data.dart';

class HumanBoneService {
  static List<HumanBoneData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadHumanBones();
    final b = dailyHumanBone(_cache!);

    final buf = StringBuffer();
    buf.writeln('🦴 Region: ${b.region}  |  Type: ${b.type}');
    buf.writeln('🔢 Count in body: ${b.count}');
    buf.writeln('⚙️ Function: ${b.function}');
    buf.writeln('💡 ${b.famousFor}');

    return ContentData(
      preview: '🦴 ${b.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: b.imageUrl,
      noImageMessage: b.noImageMessage,
    );
  }
}
