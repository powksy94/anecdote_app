import '../data/horror_cinema_data.dart';
import '../../../core/models/content_data.dart';

class HorrorCinemaService {
  static List<HorrorCinemaData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadHorrorCinema();
    final f = dailyHorrorCinema(_cache!);

    final buf = StringBuffer();
    buf.writeln('📅 Year: ${f.year}');
    buf.writeln('🎥 Director: ${f.director}');
    buf.writeln('🌍 Country: ${f.country}');
    buf.writeln('⏱️ Duration: ${f.duration} min');
    buf.writeln('💡 ${f.famousFor}');

    return ContentData(
      preview: '🎬 ${f.title} (${f.year})',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: f.imageUrl,
      noImageMessage: f.noImageMessage,
      protectedTerms: [f.title],
      filmTitleFr: f.titleFr != null ? '🎬 ${f.titleFr} (${f.year})' : null,
      filmTitleEs: f.titleEs != null ? '🎬 ${f.titleEs} (${f.year})' : null,
    );
  }
}
