import '../data/insect_data.dart';
import '../../../core/models/content_data.dart';

class InsectService {
  static List<InsectData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadInsects();
    final i = dailyInsect(_cache!);

    final buf = StringBuffer();
    buf.writeln('🔬 Order: ${i.order}  |  Family: ${i.family}');
    buf.writeln('📏 Size: ${i.size}');
    buf.writeln('🌿 Habitat: ${i.habitat}');
    buf.writeln('🍃 Diet: ${i.diet}');
    buf.writeln('💡 ${i.famousFor}');

    return ContentData(
      preview: '🦟 ${i.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: i.imageUrl,
      noImageMessage: i.noImageMessage,
    );
  }
}
