import '../data/country_data.dart';
import '../../../core/models/content_data.dart';

class CountryService {
  static List<CountryData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadCountries();
    final c = dailyCountry(_cache!);

    final flag = c.iso2.length == 2
        ? c.iso2.toUpperCase().split('').map((ch) =>
            String.fromCharCode(ch.codeUnitAt(0) - 0x41 + 0x1F1E6)).join()
        : '🌍';

    final buf = StringBuffer();
    if (c.capital.isNotEmpty) { buf.writeln('🏛️ Capital: ${c.capital}'); }
    if (c.region.isNotEmpty)  { buf.writeln('🌐 Region: ${c.region}'); }
    if (c.population != null) {
      final pop = c.population!;
      final String fmt;
      if (pop >= 1000000000) {
        fmt = '${(pop / 1e9).toStringAsFixed(1)}B';
      } else if (pop >= 1000000) {
        fmt = '${(pop / 1e6).toStringAsFixed(1)}M';
      } else if (pop >= 1000) {
        fmt = '${(pop / 1000).toStringAsFixed(0)}K';
      } else {
        fmt = '$pop';
      }
      buf.writeln('👥 Population: $fmt');
    }
    if (c.area != null) {
      buf.writeln('📐 Area: ${c.area!.toInt().toString().replaceAllMapped(RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), (m) => '${m[1]},')} km²');
    }
    if (c.gdp != null) {
      buf.writeln('💰 GDP: \$${c.gdp!.toStringAsFixed(0)}B');
    }
    if (c.currency != null) {
      final cu = c.currency!;
      buf.writeln('💱 Currency: ${cu.name} (${cu.code} ${cu.symbol})'.trim());
    }
    if (c.languages.isNotEmpty) {
      buf.writeln('🗣️ Languages: ${c.languages.join(', ')}');
    }
    if (c.lifeExpectancy != null) {
      buf.writeln('❤️ Life expectancy: ${c.lifeExpectancy!.toStringAsFixed(1)} yrs');
    }
    if (c.unemployment != null) {
      buf.writeln('📊 Unemployment: ${c.unemployment!.toStringAsFixed(1)}%');
    }

    return ContentData(
      preview: '$flag ${c.name}',
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}
