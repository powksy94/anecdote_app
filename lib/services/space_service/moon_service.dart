import '../../data/solar_moon_data.dart';
import '../../models/content_data.dart';

class MoonService {
  static List<SolarMoonData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSolarMoons();
    final m = dailySolarMoon(_cache!);

    final buf = StringBuffer();
    buf.writeln('🪐 Planet: ${m.planet}');
    buf.writeln('📏 Diameter: ${m.diameter} km');
    buf.writeln('🔄 Orbital period: ${m.orbitalPeriod.toStringAsFixed(2)} days');
    buf.writeln('📅 Discovered: ${m.discoveryYear}');
    buf.writeln('🔭 Discoverer: ${m.discoverer}');
    buf.writeln('💡 Features: ${m.features}');

    return ContentData(
      preview: '🌕 ${m.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: m.imageUrl,
      noImageMessage: m.noImageMessage,
    );
  }
}
