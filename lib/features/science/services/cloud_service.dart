import '../data/cloud_data.dart';
import '../../../core/models/content_data.dart';

class CloudService {
  static List<CloudData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadClouds();
    final c = dailyCloud(_cache!);

    final buf = StringBuffer();
    buf.writeln('☁️ Category: ${c.category}  |  Altitude: ${c.altitude}');
    buf.writeln('📐 Typical size: ${c.volume}');
    buf.writeln('🌡️ Conditions: ${c.conditions}');
    buf.writeln('👁️ Appearance: ${c.appearance}');
    buf.writeln('🌧️ Weather: ${c.weather}');
    buf.writeln('💡 ${c.famousFor}');

    return ContentData(
      preview: '☁️ ${c.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: c.imageUrl,
      noImageMessage: c.noImageMessage,
    );
  }
}
