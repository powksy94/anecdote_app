import '../data/common_health_fact_data.dart';
import '../../../core/models/content_data.dart';

class CommonHealthFactService {
  static List<CommonHealthFactData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadCommonHealthFacts();
    final f = dailyCommonHealthFact(_cache!);

    return ContentData(
      preview: '${f.title}\n\n${f.fact}',
      details: '',
      hasDetails: false,
    );
  }
}
