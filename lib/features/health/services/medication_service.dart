import '../data/medication_data.dart';
import '../../../core/models/content_data.dart';

class MedicationService {
  static List<MedicationData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadMedications();
    final m = dailyMedication(_cache!);

    final buf = StringBuffer();
    buf.writeln('💊 Family: ${m.family}');
    buf.writeln('📅 Discovered: ${m.discoveryYear}');
    buf.writeln('🔬 Mechanism: ${m.mechanism}');
    buf.writeln('💉 Administration: ${m.administration}');
    buf.writeln('🩺 Used for: ${m.indications}');
    buf.writeln('⚠️ Common side effects: ${m.sideEffects}');

    return ContentData(
      preview: '${m.name}\n\n💡 ${m.fact}',
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}
