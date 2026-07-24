import '../data/rare_disorder_data.dart';
import '../../../core/models/content_data.dart';

class RareDisorderService {
  static List<RareDisorderData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadRareDisorders();
    final d = dailyRareDisorder(_cache!);

    final buf = StringBuffer();
    buf.writeln('🔬 Discovered: ${d.discovered}');
    buf.writeln('📊 Prevalence: ${d.prevalence}');
    buf.writeln('🧬 Heredity: ${d.heredity}');
    buf.writeln('🗓️ Daily life: ${d.dailyLifeImpact}');

    return ContentData(
      preview: '${d.name}\n\n💡 ${d.fact}',
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}
