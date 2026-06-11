import '../data/bird_data.dart';
import '../../../core/models/content_data.dart';

class BirdService {
  static List<BirdData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadBirds();
    final b = dailyBird(_cache!);

    final buf = StringBuffer();
    buf.writeln('🔬 Order: ${b.order}  |  Family: ${b.family}');
    buf.writeln('📏 Size: ${b.size}');
    buf.writeln('✈️ Speed: ${b.speed}');
    buf.writeln('🌿 Habitat: ${b.habitat}');
    buf.writeln('🍃 Diet: ${b.diet}');
    buf.writeln('💡 ${b.famousFor}');

    return ContentData(
      preview: '🐦 ${b.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: b.imageUrl,
      noImageMessage: b.noImageMessage,
    );
  }
}
