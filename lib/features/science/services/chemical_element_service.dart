import '../data/chemical_element_data.dart';
import '../../../core/models/content_data.dart';

class ChemicalElementService {
  static List<ChemicalElementData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadChemicalElements();
    final e = dailyChemicalElement(_cache!);

    final buf = StringBuffer();
    buf.writeln('🔬 Symbol: ${e.symbol}  |  Atomic number: ${e.atomicNumber}');
    buf.writeln('⚖️ Atomic mass: ${e.atomicMass}');
    buf.writeln('🧊 State at room temp: ${e.state}');
    buf.writeln('🗂️ Category: ${e.category}');
    buf.writeln('📐 Group: ${e.group}  |  Period: ${e.period}');
    buf.writeln('📅 Discovered: ${e.discovered}');
    buf.writeln('👤 Discovered by: ${e.discoveredBy}');
    buf.writeln('💡 ${e.famousFor}');

    return ContentData(
      preview: '⚗️ ${e.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: e.imageUrl,
      elementSymbol: e.imageUrl == null ? e.symbol : null,
      elementAtomicNumber: e.imageUrl == null ? e.atomicNumber : null,
    );
  }
}
