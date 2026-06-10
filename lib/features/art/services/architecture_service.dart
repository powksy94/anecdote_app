import '../data/architecture_data.dart';
import '../../../core/models/content_data.dart';

class ArchitectureService {
  static List<ArchitectureData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadArchitecture();
    final a = dailyArchitecture(_cache!);

    final buf = StringBuffer();
    buf.writeln('👷 Architect: ${a.architect}');
    buf.writeln('📅 Year: ${a.year}');
    buf.writeln('🎭 Style: ${a.style}');
    buf.writeln('📍 Location: ${a.location}');
    buf.writeln('🌍 Country: ${a.country}');
    buf.writeln('💡 ${a.famousFor}');

    return ContentData(
      preview: a.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: a.imageUrl,
      noImageMessage: a.noImageMessage,
    );
  }
}
