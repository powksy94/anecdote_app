import '../../data/pacific_island_data.dart';
import '../../models/content_data.dart';

class PacificIslandsService {
  static List<PacificIslandData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadPacificIslands();
    final p = dailyPacificIsland(_cache!);

    final buf = StringBuffer();
    if (p.archipelago.isNotEmpty) { buf.writeln('🏝️ Archipelago: ${p.archipelago}'); }
    if (p.territory.isNotEmpty)   { buf.writeln('🌐 Territory: ${p.territory}'); }
    if (p.country.isNotEmpty)     { buf.writeln('🏳️ Country: ${p.country}'); }
    if (p.ocean.isNotEmpty)       { buf.writeln('🌊 Ocean: ${p.ocean}'); }
    if (p.population != null) {
      final pop = p.population!;
      final String fmt;
      if (pop >= 1000000)     { fmt = '${(pop / 1e6).toStringAsFixed(1)}M'; }
      else if (pop >= 1000)   { fmt = '${(pop / 1000).toStringAsFixed(0)}K'; }
      else                    { fmt = '$pop'; }
      buf.writeln('👥 Population: $fmt');
    }
    if (p.area != null) {
      buf.writeln('📐 Area: ${p.area!.toStringAsFixed(1)} km²');
    }

    return ContentData(
      preview: '🌺 ${p.name}',
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}