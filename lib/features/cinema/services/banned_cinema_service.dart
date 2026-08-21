import '../data/banned_cinema_data.dart';
import '../../../core/models/content_data.dart';

class BannedCinemaService {
  static List<BannedCinemaData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadBannedCinema();
    final f = dailyBannedCinema(_cache!);

    final buf = StringBuffer();
    buf.writeln('📅 Year: ${f.year}');
    buf.writeln('🎥 Director: ${f.director}');
    buf.writeln('⏱️ Duration: ${f.duration} min');
    if (f.contentTypes.isNotEmpty) {
      buf.writeln('🏷️ Content: ${f.contentTypes.join(", ")}');
    }
    buf.writeln('🚫 Banned in: ${f.bannedIn}');
    buf.writeln('💡 ${f.reason}');

    return ContentData(
      preview: '🚫 ${f.title} (${f.year})',
      details: buf.toString().trim(),
      hasDetails: true,
      protectedTerms: [f.title],
      filmTitleFr: f.titleFr != null ? '🚫 ${f.titleFr} (${f.year})' : null,
      filmTitleEs: f.titleEs != null ? '🚫 ${f.titleEs} (${f.year})' : null,
    );
  }
}
