import '../data/medical_anecdote_data.dart';
import '../../../core/models/content_data.dart';

class MedicalAnecdoteService {
  static List<MedicalAnecdoteData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadMedicalAnecdotes();
    final a = dailyMedicalAnecdote(_cache!);

    return ContentData(
      preview: '${a.title}\n\n💡 ${a.fact}\n📅 ${a.year}',
      details: '',
      hasDetails: false,
    );
  }
}
