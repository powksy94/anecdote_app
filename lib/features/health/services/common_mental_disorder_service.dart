import '../data/common_mental_disorder_data.dart';
import '../../../core/models/content_data.dart';

class CommonMentalDisorderService {
  static List<CommonMentalDisorderData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadCommonMentalDisorders();
    final d = dailyCommonMentalDisorder(_cache!);

    final buf = StringBuffer();
    buf.writeln('🔬 First described: ${d.discovered}');
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
