import '../data/legendary_athlete_data.dart';
import '../../../core/models/content_data.dart';

class LegendaryAthleteService {
  static List<LegendaryAthleteData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadLegendaryAthletes();
    final a = dailyLegendaryAthlete(_cache!);

    final buf = StringBuffer();
    buf.writeln('🌍 Country: ${a.country}');
    buf.writeln('🏅 Sport: ${a.sport}');
    buf.writeln('🗓️ Active: ${a.activeYears}');
    if (a.trophies != null) buf.writeln('🏆 ${a.trophies}');
    if (a.medals != null) buf.writeln('🥇 ${a.medals}');
    buf.writeln('💡 ${a.impact}');

    return ContentData(
      preview: a.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: a.imageUrl,
      noImageMessage: a.imageUrl == null ? '📷 No photo available for this athlete' : null,
    );
  }
}
