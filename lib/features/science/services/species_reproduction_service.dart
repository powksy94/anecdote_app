import '../data/species_reproduction_data.dart';
import '../../../core/models/content_data.dart';

class SpeciesReproductionService {
  static List<SpeciesReproductionData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSpeciesReproduction();
    final s = dailySpeciesReproduction(_cache!);

    final buf = StringBuffer();
    buf.writeln('🧬 Strategy: ${s.strategy}');
    buf.writeln('🥚 Type: ${s.type}');
    buf.writeln('⏳ Gestation: ${s.gestation}');

    return ContentData(
      preview: '${s.name}\n\n💡 ${s.fact}',
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}
